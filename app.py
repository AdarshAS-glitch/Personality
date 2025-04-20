from flask import Flask, jsonify, render_template, request, send_from_directory
import json
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Load questions from a JSON file
with open('questions.json') as f:
    questions = json.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/questions', methods=['GET'])
def get_questions():
    return jsonify(questions)

@app.route('/submit', methods=['POST'])
def submit_answers():
    data = request.json
    print("User answers:", data)

    # Dummy scoring logic (you'll improve this later)
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
