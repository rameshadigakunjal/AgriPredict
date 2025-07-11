document.addEventListener('DOMContentLoaded', () => {
    const predictionForm = document.getElementById('predictionForm');
    const predictionResults = document.getElementById('predictionResults');
    const yieldOutput = document.getElementById('yieldOutput');
    const npkOutput = document.getElementById('npkOutput');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');

    // Function to show/hide elements
    const showElement = (element) => element.classList.remove('hidden');
    const hideElement = (element) => element.classList.add('hidden');

    // Function to reset results display
    const resetResultsDisplay = () => {
        hideElement(predictionResults);
        hideElement(loadingIndicator);
        hideElement(errorMessage);
        yieldOutput.textContent = '--';
        npkOutput.textContent = 'N: -- P: -- K: --';
    };

    // Initial reset when the page loads
    resetResultsDisplay();

    // --- Recent Inputs Logic ---
    const recentInputsKey = 'recentPredictionInputs';
    const recentInputsDropdown = document.getElementById('recentInputs');

    function saveRecentInput(inputObj) {
        let recents = JSON.parse(localStorage.getItem(recentInputsKey)) || [];
        // Remove identical input if exists
        recents = recents.filter(r => JSON.stringify(r) !== JSON.stringify(inputObj));
        // Add new input to front
        recents.unshift(inputObj);
        // Keep only last 3
        recents = recents.slice(0, 3);
        localStorage.setItem(recentInputsKey, JSON.stringify(recents));
    }

    function populateRecentInputsDropdown() {
        const recents = JSON.parse(localStorage.getItem(recentInputsKey)) || [];
        recentInputsDropdown.innerHTML = '<option value="">Select a recent input...</option>';
        recents.forEach((input, idx) => {
            const label = `${input.district}, ${input.year}, Prod: ${input.production}, Area: ${input.area}, Rain: ${input.rainfall}, Temp: ${input.temperature}, Hum: ${input.humidity}`;
            const opt = document.createElement('option');
            opt.value = idx;
            opt.textContent = label;
            recentInputsDropdown.appendChild(opt);
        });
    }

    if (recentInputsDropdown) {
        populateRecentInputsDropdown();
        recentInputsDropdown.addEventListener('change', function() {
            const recents = JSON.parse(localStorage.getItem(recentInputsKey)) || [];
            const idx = parseInt(this.value);
            if (!isNaN(idx) && recents[idx]) {
                // Fill form fields
                document.getElementById('districtPredict').value = recents[idx].district;
                document.getElementById('year').value = recents[idx].year;
                document.getElementById('production').value = recents[idx].production;
                document.getElementById('area').value = recents[idx].area;
                document.getElementById('rainfall').value = recents[idx].rainfall;
                document.getElementById('temperature').value = recents[idx].temperature;
                document.getElementById('humidity').value = recents[idx].humidity;
            }
        });
    }

    // --- Prediction Form Submission ---
    if (predictionForm) {
        console.log("Form handler attached");
        predictionForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission
            console.log("Submit event fired");
            alert("Prediction form submit event fired!");

            resetResultsDisplay(); // Clear previous results and hide messages
            showElement(loadingIndicator); // Show loading indicator

            // Collect form data
            const district = document.getElementById('districtPredict').value;
            const year = document.getElementById('year').value;
            const area = parseFloat(document.getElementById('area') ? document.getElementById('area').value : 0);
            const production = parseFloat(document.getElementById('production').value);
            const temperature = parseFloat(document.getElementById('temperature').value);
            const humidity = parseFloat(document.getElementById('humidity').value);
            const rainfall = parseFloat(document.getElementById('rainfall').value);

            // Save to recent inputs
            saveRecentInput({
                district,
                year,
                production,
                area,
                rainfall,
                temperature,
                humidity
            });
            populateRecentInputsDropdown();

            // Basic client-side validation
            if (!district || !year || isNaN(production) || isNaN(rainfall) || isNaN(temperature) || isNaN(humidity)) {
                hideElement(loadingIndicator);
                showElement(errorMessage);
                errorMessage.querySelector('p').textContent = 'Please fill in all required fields with valid numbers.';
                return;
            }

            // Construct payload for the backend
            const payload = {
                district: district,
                year: parseInt(year),
                area: area,
                production: production,
                temperature: temperature,
                humidity: humidity,
                rainfall: rainfall
            };

            try {
                // Get access token from local storage (if available from login)
                const accessToken = localStorage.getItem('access_token');
                const headers = {
                    'Content-Type': 'application/json',
                };
                if (accessToken) {
                    headers['Authorization'] = `Bearer ${accessToken}`;
                }

                // Replace with your actual Flask backend prediction endpoint
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(payload),
                });

                const data = await response.json();

                hideElement(loadingIndicator); // Hide loading indicator

                if (response.ok) {
                    // Prediction successful
                    console.log('Prediction successful:', data);
                    showElement(predictionResults); // Show the results section
                    predictionResults.scrollIntoView({ behavior: 'smooth' });
                    // Update the DOM with predicted values
                    yieldOutput.textContent = `${data.predicted_yield.toFixed(2)} Kg/ha`;
                    npkOutput.textContent = `N: ${data.predicted_n.toFixed(2)} P: ${data.predicted_p.toFixed(2)} K: ${data.predicted_k.toFixed(2)}`;
                } else {
                    // Prediction failed
                    console.error('Prediction failed:', data.message || 'Unknown error');
                    showElement(errorMessage); // Show error message
                    errorMessage.querySelector('p').textContent = data.message || 'Prediction failed. Please check your inputs and try again.';
                }
            } catch (error) {
                console.error('Network error or unexpected issue during prediction:', error);
                hideElement(loadingIndicator);
                showElement(errorMessage); // Show error message
                errorMessage.querySelector('p').textContent = 'An error occurred while fetching prediction. Please try again later.';
            }
        });
    }
});
