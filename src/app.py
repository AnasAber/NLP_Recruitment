import streamlit as st
import requests, json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import extract_text


def query_groq_api(resume, job_description):
    url = "http://localhost:5000/query"
    headers = {"Content-Type": "application/json"}
    data = {
        "resume": resume,
        "job_description": job_description
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the response status code indicates success
    if response.status_code == 200:
        try:
            return response.json()        
        except json.JSONDecodeError:
            return {"error": "The server response was not valid JSON."}
    else:
        return {"error": f"Request failed with status code {response.status_code}."}
    


st.title("Resume Matching System")

st.write("Upload your resume and job description to get the matching percentage.")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_description = st.text_area("Job Description", height=200)
button = st.button("Process Resume")

if button and uploaded_resume and job_description:
    # Read and encode the resume only if a file is uploaded
    resume = extract_text(uploaded_resume)
    with st.spinner("Processing..."):
        result = query_groq_api(resume, job_description)
        result = json.loads(result["response"])

        if 'error' in result:
            st.error(result['error'])
        else:
            st.success("Processing complete!")
            st.empty()
            # Display the match percentage
            st.header("Match Percentage")
            st.write(f"Your resume matches the job description with a score of {result['Match Percentage']}%")

            # Display the extracted entities
            st.header("Extracted Entities")
            st.subheader("Experience")
            st.write(result["Extracted Entities"]["Experience"])
            st.subheader("Competence")
            st.write(result["Extracted Entities"]["Competence"])
            st.subheader("Qualifications")
            st.write(result["Extracted Entities"]["Qualifications"])

            # Display the missing keywords/skills
            st.header("Missing Keywords/Skills")
            st.write(result["Missing Keywords/Skills"])

            # Display the final thoughts
            st.header("Final Thoughts")
            st.write(result["Final Thoughts"])
else:
    st.warning("Please upload a resume to continue.")

