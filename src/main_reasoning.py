import json

import dotenv
import streamlit as st
from flask import Flask, jsonify, request

from models.functions import (
    get_job_details,
    get_matching_score,
    get_resume_details,
    resume_details_builder,
    generate_questions
)

dotenv.load_dotenv()

app = Flask(__name__)

response_text_job = ""
response_text_resume = ""


@app.route("/query", methods=["POST"])
def query():
    data = request.json
    job_description = data.get("job_description")
    resume_text = data.get("resume")

    if not job_description:
        print("job is empty am3llem")
        return jsonify({"error": "No query provided"}), 400

    if not resume_text:
        print("resume is empty am3llem")
        return jsonify({"error": "No resume provided"}), 400

    # this one is the text that will be used to query the model, the TEXT_GENERATION_PROMPT is a template that will be filled with the job description and the resume

    global response_text_job
    global response_text_resume

    response_text_resume = get_resume_details(resume_text)
    response_text_job = get_job_details(job_description)
    scores = get_matching_score(response_text_job, response_text_resume)


    try:
        return jsonify({"response": scores})
    except Exception as e:
        return jsonify({"error": "error sending scores"}), 500

@app.route("/questions", methods=["POST"])
def questions():
    data = request.json
    job_description = data.get("job_description")
    resume_text = data.get("resume_details")

    print(f"this is the resume text I got:\
          {resume_text}\
        ")
    print(f"this is the job description I got:\
          {job_description}\
        ")
    
    questions = generate_questions(response_text_resume, response_text_job)
    
    print(f"this is the questions I sent!:\
          {questions}\n\n                 \
        ")
    
    questions = json.loads(questions)

    try:
        return jsonify({"response": questions})
    except:
        return jsonify({"error": " error sending questions! "})




if __name__ == "__main__":
    app.run(debug=True)
