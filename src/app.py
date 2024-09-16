import streamlit as st
import requests, json, os, sys

# Append the utils path to system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import extract_text

# Function to query the resume matching API
def query_groq_api(resume, job_description):
    url = "http://localhost:5000/query"
    headers = {"Content-Type": "application/json"}
    data = {"resume": resume, "job_description": job_description}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "The server response was not valid JSON."}
    else:
        return {"error": f"Request failed with status code {response.status_code}."}

# Page configuration
st.set_page_config(page_title="Job Hunting Assistant")

# Initialize session state for tracking the match percentage and page state
if "match_percentage" not in st.session_state:
    st.session_state["match_percentage"] = None  # Track match percentage
if "page" not in st.session_state:
    st.session_state["page"] = "matching"  # Default page

# Handle page switching based on session state
if st.session_state["page"] == "interview":
    st.switch_page("pages/interview.py")

else:
    # Main page (Resume Matching System)
    st.title("Resume Matching System")
    st.write("Upload your resume and job description to get the matching percentage.")

    # Upload the resume and input job description
    uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
    job_description = st.text_area("Job Description", height=200)
    button = st.button("Process Resume")

    if button and uploaded_resume and job_description:
        uploaded_resume.seek(0)
        resume = extract_text(uploaded_resume)

        # Store the resume and job description in session state
        st.session_state["resume"] = resume
        st.session_state["job_description"] = job_description

        with st.spinner("Processing..."):
            results = query_groq_api(resume, job_description)

            if "error" in results:
                st.error(results["error"])
            else:
                result = json.loads(results["response"]) if isinstance(results["response"], str) else results["response"]

                if "Match Percentage" in result:
                    match_percentage = result['Match Percentage']
                    st.session_state["match_percentage"] = match_percentage

                    st.header("Match Percentage")
                    st.progress(match_percentage / 100)  # Progress bar
                    st.write(f"**Your resume matches the job description with a score of `{match_percentage}%`**")

                    st.header("Extracted Entities")
                    st.markdown("### **Experience**")
                    st.write(result["Extracted Entities"].get("Experience", "N/A"))

                    st.markdown("### **Competence**")
                    st.write(result["Extracted Entities"].get("Competence", "N/A"))

                    st.markdown("### **Qualifications**")
                    st.write(result["Extracted Entities"].get("Qualifications", "N/A"))

                    st.header("Missing Keywords/Skills")
                    if result.get("Missing Keywords/Skills"):
                        st.warning("Some keywords or skills are missing!")
                        st.write(result["Missing Keywords/Skills"])
                    else:
                        st.success("No missing keywords or skills!")

                    st.header("Final Thoughts")
                    st.info(result.get("Final Thoughts", "No additional comments."))

                else:
                    st.error("No valid match percentage returned in the response.")

    if st.session_state["match_percentage"] is not None:
        if st.session_state["match_percentage"] >= 60:
            if st.button("Are you ready to take an interview?", key="interview_button"):
                st.session_state["page"] = "interview"
                st.experimental_rerun()
        else:
            st.warning(f"\n Unfortunately, You're not a match to this job description, you can find better 🥀 ")
