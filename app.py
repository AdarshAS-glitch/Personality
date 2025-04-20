from flask import Flask, jsonify, render_template, request, send_from_directory
import json
from flask_cors import CORS
import os
from collections import defaultdict
import random

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
big_five = {
    "Extraversion": [1, 15, 24, 35, 50, 52, 67, 70, 104, 112, 124, 131, 145, 154, 161, 175],
    "Conscientiousness": [2, 8, 18, 21, 26, 30, 32, 39, 47, 49, 60, 63, 77, 80, 84, 87, 94, 99, 100, 102, 107, 120, 126, 129, 132, 138, 148, 151, 156, 162, 168, 178],
    "Agreeableness": [3, 6, 9, 16, 23, 27, 34, 48, 58, 62, 68, 69, 74, 79, 82, 91, 101, 109, 114, 117, 123, 127, 130, 133, 136, 139, 146, 153, 157, 163, 166, 169, 176],
    "Openness": [4, 10, 12, 14, 17, 19, 25, 28, 29, 36, 38, 41, 42, 44, 54, 61, 65, 66, 71, 75, 81, 83, 85, 86, 90, 95, 97, 98, 103, 108, 110, 111, 115, 116, 118, 122, 128, 134, 140, 142, 144, 147, 149, 155, 158, 159, 164, 170, 172, 174, 177, 179],
    "Neuroticism": [5, 11, 13, 20, 31, 37, 40, 43, 45, 46, 53, 55, 56, 59, 72, 73, 76, 78, 89, 93, 96, 105, 113, 118, 125, 135, 141, 143, 150, 165, 171, 173, 180]
}
selecting1=random.sample(big_five["Extraversion"],12)
selecting2=random.sample(big_five["Conscientiousness"],12)
selecting3=random.sample(big_five["Agreeableness"],12)
selecting4=random.sample(big_five["Openness"],13)
selecting5=random.sample(big_five["Neuroticism"],13)
final_selection_big_5=selecting1+selecting2+selecting3+selecting4+selecting5


# MBTI Dichotomies
mbti = {
    "E": [1, 15, 24, 35, 50, 52, 67, 70, 92, 104, 112, 124, 131, 145, 154, 161, 175],
    "I": [7, 22, 51, 56, 105, 119, 121, 137, 152, 167],
    "S": [12, 38, 41, 49, 65, 71, 83, 86, 95, 106, 111, 116, 118, 142, 172],
    "N": [4, 10, 14, 17, 19, 25, 28, 36, 42, 44, 54, 61, 66, 75, 81, 85, 97, 98, 103, 108, 110, 115, 122, 128, 134, 140, 144, 147, 149, 155, 158, 164, 170, 174, 177, 179],
    "T": [5, 11, 29, 36, 57, 68, 69, 76, 82, 85, 91, 96, 109, 113, 141, 159, 171],
    "F": [3, 6, 9, 13, 16, 23, 27, 33, 34, 37, 40, 46, 48, 58, 62, 70, 74, 79, 88, 101, 114, 117, 119, 123, 127, 130, 133, 136, 139, 143, 146, 153, 157, 163, 166, 169, 173, 176],
    "J": [2, 8, 18, 21, 26, 30, 32, 39, 43, 45, 47, 53, 59, 60, 63, 64, 77, 80, 84, 87, 94, 99, 100, 102, 107, 120, 126, 129, 132, 138, 148, 151, 156, 162, 168, 178],
    "P": [7, 22, 28, 42, 55, 72, 78, 81, 90, 93, 103, 105, 115, 121, 125, 137, 152, 158, 160, 167, 170]
}
selecting1 = random.sample(mbti["E"], 8)
selecting2 = random.sample(mbti["I"], 8)
selecting3 = random.sample(mbti["S"], 8)
selecting4 = random.sample(mbti["N"], 7)
selecting5 = random.sample(mbti["T"], 8)
selecting6 = random.sample(mbti["F"], 7)
selecting7 = random.sample(mbti["J"], 8)
selecting8 = random.sample(mbti["P"], 8)
final_selection_mbti = selecting1 + selecting2 + selecting3 + selecting4 + selecting5 + selecting6 + selecting7 + selecting8


# Enneagram Types
enneagram = {
    "1": [2, 18, 21, 26, 31, 32, 49, 53, 60, 69, 77, 94, 106, 126, 148, 151, 156, 162],
    "2": [3, 6, 9, 16, 23, 48, 62, 74, 84, 92, 101, 117, 127, 133, 136, 146, 153, 163, 166, 176],
    "3": [1, 8, 24, 40, 70, 87, 100, 116, 120, 124, 138, 154, 161, 168],
    "4": [14, 17, 19, 20, 33, 37, 46, 54, 56, 88, 98, 110, 119, 122, 144, 149, 150, 174, 177, 179, 180],
    "5": [4, 10, 19, 29, 36, 44, 61, 66, 75, 83, 85, 93, 102, 128, 134, 140, 147, 159, 164, 171],
    "6": [5, 12, 41, 43, 45, 59, 65, 71, 73, 78, 80, 91, 99, 118, 125, 129, 135, 142, 165, 172],
    "7": [25, 28, 38, 42, 50, 52, 55, 67, 81, 90, 97, 103, 108, 112, 131, 155, 158, 170],
    "8": [15, 35, 57, 64, 68, 82, 95, 104, 109, 145, 175],
    "9": [27, 30, 34, 47, 58, 72, 79, 96, 105, 113, 114, 123, 130, 139, 157, 160, 169]
}

# Pre-selected 60 questions with even distribution
enneagram_selection = (
    random.sample(enneagram["1"], 7) +
    random.sample(enneagram["2"], 7) +
    random.sample(enneagram["3"], 7) +
    random.sample(enneagram["4"], 7) +
    random.sample(enneagram["5"], 7) +
    random.sample(enneagram["6"], 7) +
    random.sample(enneagram["7"], 7) +
    random.sample(enneagram["8"], 7) +
    random.sample(enneagram["9"], 7)
)
choice=random.randint(1,3)
print(f"Randomly selected choice: {choice}")
match choice:
    case 1:
        selected_ids = final_selection_mbti
    case 2:
        selected_ids = final_selection_big_5
    case 3:
        selected_ids = enneagram_selection
    case _:
        selected_ids = []  # Optional: default case




print(selected_ids)

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