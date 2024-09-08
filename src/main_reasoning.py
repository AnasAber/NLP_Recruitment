from flask import Flask, request, jsonify
import dotenv
import streamlit as st
import json, re
from models.functions import get_resume_details, resume_details_builder, get_job_details, get_matching_score, generate_questions, get_answers_score
    
dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    job_description = data.get('job_description')
    resume_text = data.get('resume')

    
    if not job_description:
        print("job is empty am3llem")
        return jsonify({"error": "No query provided"}), 400
    
    if not resume_text:
        print("resume is empty am3llem")
        return jsonify({"error": "No resume provided"}), 400
    
    response_text_resume = get_resume_details(resume_text)
    global response_text_job
    response_text_job = get_job_details(job_description)
    response_text = response_text_resume + response_text_job
    # response_text = resume_details_builder(response_text_job, response_text_resume)
    scores = get_matching_score(response_text, resume_text)
    scores_json = json.loads(scores)
    if scores_json["Match Percentage"] > 60:
        st.write(f"\n Your resume matches the job description with a score of {scores_json['Match Percentage']} %")
    else:
        scores = "You're not a match to this job description"

    try:
        return jsonify({"response": scores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/questions', methods=['POST'])
def questions():
    data = request.json
    resume_text = data.get("resume_details") # text
    job_desc = data.get("job_description") # text
    job_desc = get_job_details(job_desc)
    if resume_text:
        questions = generate_questions(resume_text, job_desc)
        questions_json = json.loads(questions)
        question_counts = {"hard": 0, "medium": 0, "low/easy": 0}

        for question in questions_json:
            level = question["level"]
            if level == "low" or level == "easy":
                level = "low/easy"
            question_counts[level] += 1

        print(question_counts)
        try:
            return jsonify({"response": questions})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        


# @app.route('/answers', methods=['POST'])
# def query_answer():
#     data = request.json
#     questions = data.get("questions")
#     answers = data.get("answers")

#     # response_text = get_answers_score(questions, answers)
#     # response_text = get_questions_score(response_text)
#     # response_text = get_summary(response_text)

#     try:
#         return jsonify({"response": questions})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)
