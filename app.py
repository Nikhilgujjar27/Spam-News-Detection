from flask import Flask, render_template, request, jsonify
import pickle
import joblib  # Added joblib support
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import pandas as pd
import os
import sys
import sklearn

app = Flask(__name__)

# Initialize stemmer
ps = PorterStemmer()

# Load the trained model and vectorizer with EXTREME debugging
model = None
vectorizer = None

print("=" * 60)
print("MODEL LOADING DEBUG INFORMATION")
print("=" * 60)

# Check current environment
print(f"Python version: {sys.version}")
print(f"scikit-learn version: {sklearn.__version__}")

# Check file existence with absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
model_folder = os.path.join(current_dir, 'model')

print(f"Model folder: {model_folder}")
print(f"Current directory: {current_dir}")

# Check if model folder exists
if not os.path.exists(model_folder):
    print("Model folder does not exist! Creating it...")
    os.makedirs(model_folder)

# Define all possible file paths
model_paths = {
    'joblib_model': os.path.join(model_folder, 'trained_model.joblib'),
    'joblib_vectorizer': os.path.join(model_folder, 'tfidf_vectorizer.joblib'),
    'pickle_model': os.path.join(model_folder, 'trained_model.pkl'),
    'pickle_vectorizer': os.path.join(model_folder, 'tfidf_vectorizer.pkl')
}

# Check which files exist
print("\nChecking for model files:")
for name, path in model_paths.items():
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    print(f"   {name}: {'✅' if exists else '❌'} {path}")
    if exists:
        print(f"        Size: {size} bytes")

# Try to load files - JOBLIB FIRST (better compatibility)
print("\n Attempting to load model files...")

# Try joblib first
try:
    if os.path.exists(model_paths['joblib_model']) and os.path.exists(model_paths['joblib_vectorizer']):
        print("Trying to load with joblib...")
        model = joblib.load(model_paths['joblib_model'])
        vectorizer = joblib.load(model_paths['joblib_vectorizer'])
        print("Successfully loaded with joblib!")
        print(f"   Model type: {type(model)}")
        print(f"   Vectorizer type: {type(vectorizer)}")
    else:
        print("ℹ  Joblib files not found, trying pickle...")
        raise FileNotFoundError("Joblib files not available")

except Exception as e:
    print(f" Joblib loading failed: {str(e)}")
    print(" Falling back to pickle...")

    # Try pickle as fallback
    try:
        if os.path.exists(model_paths['pickle_model']) and os.path.exists(model_paths['pickle_vectorizer']):
            with open(model_paths['pickle_model'], 'rb') as f:
                model = pickle.load(f)
            with open(model_paths['pickle_vectorizer'], 'rb') as f:
                vectorizer = pickle.load(f)
            print(" Successfully loaded with pickle!")
            print(f"   Model type: {type(model)}")
            print(f"   Vectorizer type: {type(vectorizer)}")
        else:
            print(" Pickle files also not found!")
            raise FileNotFoundError("No model files found")

    except Exception as e2:
        print(f" Pickle loading also failed: {str(e2)}")
        print(" All loading methods failed. Possible solutions:")
        print("   1. Train model directly in this environment")
        print("   2. Check version compatibility")
        print("   3. Ensure files are not corrupted")
        model = None
        vectorizer = None

print("=" * 60)


# Text preprocessing function
def preprocess_text(content):
    try:
        if not isinstance(content, str):
            content = str(content)

        stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
        stemmed_content = stemmed_content.lower()
        stemmed_content = stemmed_content.split()
        stemmed_content = [ps.stem(word) for word in stemmed_content
                           if not word in stopwords.words('english')]
        stemmed_content = ' '.join(stemmed_content)
        return stemmed_content
    except Exception as e:
        print(f"Text processing error: {e}")
        return ""


@app.route('/')
def home():
    status_message = " Model loaded successfully!" if model and vectorizer else "⚠️ Model not loaded. Check terminal for errors."
    return render_template('index.html',
                           model_loaded=bool(model and vectorizer),
                           message=status_message)


@app.route('/predict', methods=['POST'])
def predict():
    if model is None or vectorizer is None:
        return jsonify({
            'error': 'Model not available',
            'message': 'The AI model is not loaded. Please check the terminal for detailed error messages.',
            'debug_info': {
                'model_loaded': model is not None,
                'vectorizer_loaded': vectorizer is not None,
                'files_found': {
                    'joblib_model': os.path.exists(model_paths['joblib_model']),
                    'joblib_vectorizer': os.path.exists(model_paths['joblib_vectorizer']),
                    'pickle_model': os.path.exists(model_paths['pickle_model']),
                    'pickle_vectorizer': os.path.exists(model_paths['pickle_vectorizer'])
                }
            }
        })

    try:
        news_content = request.form['news_content']

        if not news_content.strip():
            return jsonify({'error': 'Please enter some news content'})

        processed_text = preprocess_text(news_content)

        if len(processed_text.strip()) < 3:
            return jsonify({'error': 'Text too short after processing'})

        text_vector = vectorizer.transform([processed_text])
        prediction = model.predict(text_vector)
        confidence = model.predict_proba(text_vector).max()

        result = "Real News" if prediction[0] == 1 else "Fake News"

        return jsonify({
            'prediction': result,
            'confidence': round(confidence * 100, 2),
            'processed_text': processed_text[:200] + '...' if len(processed_text) > 200 else processed_text
        })

    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'})


if __name__ == '__main__':
    # Download stopwords
    try:
        nltk.data.find('corpora/stopwords')
        print(" NLTK stopwords available")
    except LookupError:
        print(" Downloading NLTK stopwords...")
        nltk.download('stopwords')

    # Final status
    if model and vectorizer:
        print(" Server ready with loaded model!")
        print(" Starting Flask server at http://localhost:5000")
    else:
        print(" Server starting WITHOUT model functionality")
        print(" You can still run the app, but predictions won't work")

    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)