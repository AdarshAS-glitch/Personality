// Fetch questions from Flask backend
async function loadQuestions() {
    try {
        const response = await fetch('/questions');
        const questions = await response.json();

        const questionsContainer = document.getElementById('questions');
        questionsContainer.innerHTML = '';  // Clear existing questions

        // Create HTML elements for each question
        questions.forEach(q => {
            const questionElement = document.createElement('div');
            questionElement.classList.add('question');

            const label = document.createElement('label');
            label.innerText = q.text;

            const input = document.createElement('input');
            input.type = 'range';
            input.min = 1;
            input.max = 5;
            input.name = q.id; // Store question ID for tracking

            questionElement.appendChild(label);
            questionElement.appendChild(input);
            questionsContainer.appendChild(questionElement);
        });
    } catch (error) {
        console.error('Error loading questions:', error);
    }
}

// Function to collect answers and submit them
async function submitAnswers() {
    const answers = {};
    const inputs = document.querySelectorAll('#questions input');

    inputs.forEach(input => {
        answers[input.name] = input.value;
    });

    // Send answers to Flask backend
    try {
        const response = await fetch('/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(answers),
        });

        const result = await response.json();
        alert(`Your MBTI: ${result.mbti}, Enneagram: ${result.enneagram}, Big Five: ${JSON.stringify(result.big_five)}`);
    } catch (error) {
        console.error('Error submitting answers:', error);
    }
}

// Load questions when the page is ready
window.onload = loadQuestions;
