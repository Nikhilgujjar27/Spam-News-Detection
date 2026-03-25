document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('newsForm');
    const resultSection = document.getElementById('resultSection');
    const loading = document.getElementById('loading');
    const newsContent = document.getElementById('newsContent');

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Show loading, hide results
        loading.style.display = 'block';
        resultSection.style.display = 'none';

        // Send prediction request
        fetch('/predict', {
            method: 'POST',
            body: new FormData(form)
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            loading.style.display = 'none';

            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            // Display results
            const resultIcon = document.getElementById('resultIcon');
            const predictionText = document.getElementById('predictionText');
            const confidenceValue = document.getElementById('confidenceValue');
            const processedText = document.getElementById('processedText');

            predictionText.textContent = data.prediction;
            confidenceValue.textContent = data.confidence;
            processedText.textContent = data.processed_text;

            // Set appropriate icon and color
            if (data.prediction === "Real News") {
                resultIcon.innerHTML = "✅";
                resultIcon.style.color = "#28a745";
                predictionText.style.color = "#28a745";
            } else {
                resultIcon.innerHTML = "❌";
                resultIcon.style.color = "#dc3545";
                predictionText.style.color = "#dc3545";
            }

            // Show result section
            resultSection.style.display = 'block';
        })
        .catch(error => {
            loading.style.display = 'none';
            alert('Error: ' + error);
        });
    });

    // Analyze another news button
    document.getElementById('analyzeAnotherBtn').addEventListener('click', function() {
        resultSection.style.display = 'none';
        newsContent.value = '';
        newsContent.focus();
    });
});