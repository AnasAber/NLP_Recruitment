import json
import dotenv
import streamlit as st
from flask import Flask, jsonify, request

from models.functions import (
    get_job_details,
    get_matching_score,
    get_resume_details,
    generate_questions,
    get_answers_score
)

dotenv.load_dotenv()

app = Flask(__name__)

response_text_job = ""
response_text_resume = ""

@app.route("/query", methods=["POST"])
def query_scores():
    data = request.json
    job_description = data.get("job_description")
    resume_text = data.get("resume")

    if not job_description:
        return jsonify({"error": "No job description provided"}), 400

    if not resume_text:
        return jsonify({"error": "No resume provided"}), 400

    global response_text_job
    global response_text_resume

    response_text_resume = get_resume_details(resume_text)
    response_text_job = get_job_details(job_description)
    scores = get_matching_score(response_text_job, response_text_resume)

    try:
        return jsonify({"response": scores})
    except Exception as e:
        return jsonify({"error": "Error sending scores"}), 500

@app.route("/questions", methods=["POST"])
def generate_interview_questions():
    data = request.json
    job_description = data.get("job_description")
    resume_text = data.get("resume_details")

    if not resume_text or not job_description:
        return jsonify({"error": "Resume details or job description not provided"}), 400

    questions = generate_questions(response_text_resume, response_text_job)
    
    try:
        # Ensure questions are in JSON format
        questions = json.loads(questions)
        return jsonify({"response": questions})
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding questions JSON"}), 500
    except Exception as e:
        return jsonify({"error": "Error sending questions"}), 500

@app.route("/score", methods=["POST"])
def score_answers():
    try:
        data = request.get_json()  # Ensure this is a dictionary with 'questions' and 'responses'
        question = data.get('question', '')
        response = data.get('response', {})

        score = get_answers_score(question, response)
        return jsonify({"response": score}), 200

    except Exception as e:
        print(f"Error in /score endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
