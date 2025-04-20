from flask import Flask, jsonify, render_template, request, send_from_directory
import json
from flask_cors import CORS
import os
from collections import defaultdict

app = Flask(__name__, static_folder='static')
CORS(app)

# Load questions from JSON file
try:
    with open('questions.json') as f:
        all_questions = json.load(f)
    print(f"Successfully loaded {len(all_questions)} questions")
except Exception as e:
    print(f"Error loading questions: {e}")
    all_questions = []

# Pre-selected 60 questions with even distribution
selected_ids = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,  
    11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    22, 24, 25, 26, 27, 28, 29, 30, 31, 32,
    33, 34, 35, 36, 37, 38, 39, 40, 41, 42,
    43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
    53, 54, 55, 56, 57, 58, 59, 60, 61, 62
]

selected_questions = [q for q in all_questions if q['id'] in selected_ids]
print(f"Selected {len(selected_questions)} questions for the test")

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/questions', methods=['GET'])
def get_questions():
    try:
        if not selected_questions:
            return jsonify({"error": "No questions available"}), 500
        return jsonify(selected_questions)
    except Exception as e:
        print(f"Error in get_questions: {e}")
        return jsonify({"error": str(e)}), 500

def calculate_scores(answers):
    """Calculate scores for all three models based on user answers"""
    # Initialize score trackers
    scores = {
        'big_five': defaultdict(int),
        'mbti': defaultdict(int),
        'enneagram': defaultdict(int)
    }
    
    # Count responses per category
    for answer in answers:
        question_id = answer['questionId']
        response = answer['response']  # Assuming 1-5 scale (1=Strongly Disagree, 5=Strongly Agree)
        
        # Find the question in our selected set
        question = next((q for q in selected_questions if q['id'] == question_id), None)
        if not question:
            continue
            
        # Big Five scoring
        if 'big_five' in question:
            scores['big_five'][question['big_five']] += response
            
        # MBTI scoring
        if 'mbti' in question:
            scores['mbti'][question['mbti']] += response
            
        # Enneagram scoring
        if 'enneagram' in question:
            scores['enneagram'][f"Type {question['enneagram']}"] += response
    
    return scores

def determine_mbti(scores):
    """Convert MBTI scores to a 4-letter type"""
    mbti = ''
    # Extraversion (E) vs Introversion (I)
    mbti += 'E' if scores['mbti']['E'] > scores['mbti']['I'] else 'I'
    # Sensing (S) vs Intuition (N)
    mbti += 'S' if scores['mbti']['S'] > scores['mbti']['N'] else 'N'
    # Thinking (T) vs Feeling (F)
    mbti += 'T' if scores['mbti']['T'] > scores['mbti']['F'] else 'F'
    # Judging (J) vs Perceiving (P)
    mbti += 'J' if scores['mbti']['J'] > scores['mbti']['P'] else 'P'
    return mbti

def determine_enneagram(scores):
    """Find the highest scoring Enneagram type"""
    enneagram_scores = scores['enneagram']
    return max(enneagram_scores.items(), key=lambda x: x[1])[0]

@app.route('/submit', methods=['POST'])
def submit_answers():
    try:
        data = request.json
        print("User answers:", data)
        
        # Calculate raw scores
        scores = calculate_scores(data['answers'])
        
        # Determine results
        mbti = determine_mbti(scores)
        enneagram = determine_enneagram(scores)
        
        # Normalize Big Five scores to 0-100 scale
        big_five = {}
        for trait, score in scores['big_five'].items():
            # Count how many questions were asked for this trait
            trait_questions = sum(1 for q in selected_questions if q['big_five'] == trait)
            # Max possible score is 5 (max response) * number of questions for this trait
            max_score = 5 * trait_questions
            # Ensure we don't divide by zero
            if max_score > 0:
                normalized = min(100, int((score / max_score) * 100))
            else:
                normalized = 0
            big_five[trait] = normalized
        
        return jsonify({
            "mbti": mbti,
            "enneagram": enneagram,
            "big_five": big_five,
            "success": True
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)