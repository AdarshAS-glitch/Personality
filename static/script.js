// Base URL for API requests
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:5000' 
    : '';

async function loadQuestions() {
    try {
        console.log('Fetching questions...');
        const res = await fetch(`${API_BASE_URL}/questions`);
        
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        
        const questions = await res.json();
        console.log('Received questions:', questions);
        
        if (!questions || questions.length === 0) {
            throw new Error('No questions received from server');
        }

        const form = document.getElementById('testForm');
        form.innerHTML = ''; // Clear any existing content

        questions.forEach(q => {
            const questionContainer = document.createElement('div');
            questionContainer.className = 'question-container';

            const questionText = document.createElement('div');
            questionText.className = 'question-text';
            questionText.textContent = q.text;
            questionContainer.appendChild(questionText);

            const ratingScale = document.createElement('div');
            ratingScale.className = 'rating-scale';
            ratingScale.innerHTML = `
                <span class="rating-option">1 (Strongly Disagree)</span>
                <span class="rating-option">2</span>
                <span class="rating-option">3 (Neutral)</span>
                <span class="rating-option">4</span>
                <span class="rating-option">5 (Strongly Agree)</span>
            `;
            questionContainer.appendChild(ratingScale);

            const input = document.createElement('input');
            input.type = 'range';
            input.min = 1;
            input.max = 5;
            input.value = 3;
            input.name = q.id;
            input.className = 'rating-slider';
            questionContainer.appendChild(input);

            form.appendChild(questionContainer);
        });

        console.log('Questions loaded successfully');
    } catch (error) {
        console.error('Error loading questions:', error);
        const form = document.getElementById('testForm');
        form.innerHTML = `
            <div class="error-message">
                <p>Error loading questions: ${error.message}</p>
                <p>Please make sure you are running the Flask server and accessing the page through http://localhost:5000</p>
                <p>To run the server, use: <code>python app.py</code></p>
            </div>
        `;
    }
}

async function submitAnswers() {
    try {
        const inputs = document.querySelectorAll('input[type="range"]');
        const answers = Array.from(inputs).map(input => ({
            questionId: parseInt(input.name),
            response: parseInt(input.value)
        }));

        const res = await fetch(`${API_BASE_URL}/submit`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answers })
        });

        const result = await res.json();
        displayResults(result);
    } catch (error) {
        console.error('Error submitting answers:', error);
        alert('Error submitting answers. Please make sure you are running the Flask server and accessing the page through http://localhost:5000');
    }
}

function displayResults(result) {
    const resultsContainer = document.getElementById('results');
    const mbtiResult = document.getElementById('mbtiResult');
    const enneagramResult = document.getElementById('enneagramResult');
    const bigFiveResult = document.getElementById('bigFiveResult');

    // Display MBTI result
    mbtiResult.innerHTML = `
        <h3>MBTI Type</h3>
        <p>Your MBTI type is: <strong>${result.mbti}</strong></p>
    `;

    // Display Enneagram result
    enneagramResult.innerHTML = `
        <h3>Enneagram Type</h3>
        <p>Your Enneagram type is: <strong>${result.enneagram}</strong></p>
    `;

    // Display Big Five results with progress bars
    let bigFiveHTML = '<h3>Big Five Personality Traits</h3>';
    for (const [trait, score] of Object.entries(result.big_five)) {
        bigFiveHTML += `
            <div class="trait-container">
                <p>${trait}: ${score}%</p>
                <div class="big-five-bar">
                    <div class="bar-fill" style="width: ${score}%"></div>
                </div>
            </div>
        `;
    }
    bigFiveResult.innerHTML = bigFiveHTML;

    // Show results container
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

// Load questions when the page loads
document.addEventListener('DOMContentLoaded', loadQuestions); 