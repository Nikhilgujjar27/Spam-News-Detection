# Spam News Detection using Machine Learning

## Overview

This project is designed to classify news articles as **real** or **spam (fake news)** using machine learning techniques. It utilizes natural language processing (NLP) to process textual data and provide accurate predictions through a web-based interface.

---

## Project Structure

```
Spam-News-Detection/
│── .idea/             # Project configuration files
│── data/              # Dataset files
│── model/             # Trained machine learning models
│── static/            # Static files (CSS, JS, images)
│── templates/         # HTML templates (frontend)
│── app.py             # Main application file (Flask app)
│── README.md
```

---

## System Workflow

The application follows these steps:

1. Input news text from the user
2. Preprocess the text (cleaning, stopword removal, normalization)
3. Convert text into numerical features using vectorization
4. Load the trained machine learning model
5. Predict whether the news is **Real** or **Spam**
6. Display the result on the web interface

---

## Data Preprocessing

* Removal of stopwords
* Cleaning text (punctuation and special characters)
* Conversion to lowercase

---

## Feature Extraction

Text data is converted into numerical form using:

* TF-IDF Vectorizer
* Count Vectorizer

---

## Model Training

The model is trained using:

* Logistic Regression
* Naive Bayes

---

## Technologies Used

* Python
* Flask (for web application)
* Scikit-learn
* Pandas
* NumPy

---

## Installation and Usage

Clone the repository:

```bash
git clone https://github.com/Nikhilgujjar27/Spam-News-Detection.git
```

Navigate to the project directory:

```bash
cd Spam-News-Detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## Features

* Web-based interface for user input
* Real-time prediction of news
* Simple and user-friendly design
* Efficient text classification

---

## Future Enhancements

* Improve model accuracy with advanced algorithms
* Deploy the application on cloud platforms
* Add support for real-time news APIs
* Enhance UI/UX design

---

## Contributing

Contributions are welcome. Please fork the repository and submit a pull request.

---

## License

This project is open-source and available under the MIT License.
