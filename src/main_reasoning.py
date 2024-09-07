import json

import dotenv
import streamlit as st
from flask import Flask, jsonify, request

from models.functions import (
    get_job_details,
    get_matching_score,
    get_resume_details,
    resume_details_builder,
)

dotenv.load_dotenv()

app = Flask(__name__)


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

    response_text_resume = get_resume_details(resume_text)
    response_text_job = get_job_details(job_description)
    response_text = response_text_resume + response_text_job
    # response_text = resume_details_builder(response_text_job, response_text_resume)
    scores = get_matching_score(response_text, resume_text)
    scores_json = json.loads(scores)
    if scores_json["Match Percentage"] > 60:
        st.write(
            f"\n Your resume matches the job description with a score of {scores_json['Match Percentage']} %"
        )
        # response_text = get_questions(response_text)
        # response_text = get_answers(response_text)
        # response_text = get_questions_score(response_text)
        # response_text = get_summary(response_text)
    else:
        scores = "You're not a match to this job description"

    try:
        return jsonify({"response": scores})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
