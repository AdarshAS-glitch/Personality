from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load questions from JSON file
try:
    with open('questions.json') as f:
        questions = json.load(f)
except Exception as e:
    print(f"Error loading questions: {e}")
    questions = []

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)  # Return questions as JSON

@app.route('/submit', methods=['POST'])
def submit_answers():
    data = request.json
    print("User answers:", data)

    # Dummy scoring logic (you'll improve this later!)
    mbti = "ENFP"
    enneagram = "Type 7"
    big_five = {
        "Openness": 75,
        "Conscientiousness": 60,
        "Extraversion": 80,
        "Agreeableness": 65,
        "Neuroticism": 55
    }

    return jsonify({
        "mbti": mbti,
        "enneagram": enneagram,
        "big_five": big_five
    })

if __name__ == '__main__':
    app.run(debug=True)
