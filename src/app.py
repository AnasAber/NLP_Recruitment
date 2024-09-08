import streamlit as st
import requests, json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import extract_text_from_pdf, extract_text


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
    

def query_groq_quest_api(resume, job_description):
    url = "http://localhost:5000/questions"
    headers = {"Content-Type": "application/json"}
    data = {
    "resume_details": resume, # a JSON string
    "job_description": job_description # text
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
    
# def query_groq_answers_api(answers, questions):
#     url = "http://localhost:5000/answers"
#     headers = {"Content-Type": "application/json"}
#     data = {
#     "questions": questions,
#     "answers": answers
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(data))

#     # Check if the response status code indicates success
#     if response.status_code == 200:
#         try:
#             return response.json()        
#         except json.JSONDecodeError:
#             return {"error": "The server response was not valid JSON."}
#     else:
#         return {"error": f"Request failed with status code {response.status_code}."}
    

st.title("Resume Matching System")

st.write("Upload your resume and job description to get the matching percentage.")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_description = st.text_area("Job Description", height=200)

if uploaded_resume is not None:
    # Read and encode the resume only if a file is uploaded
    resume = extract_text(uploaded_resume)
    with st.spinner("Processing..."):
        results = query_groq_api(resume, job_description)
        result = json.loads(results["response"])

        if 'error' in result:
            st.error(result['error'])
        else:
            clearing = st.empty()
            st.success("Processing complete!")
            clearing.empty()
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
        
        st.header("Loading Questions...")
        qst = query_groq_quest_api(resume, job_description)
        questions = json.loads(qst["response"])
        clearing.empty()


        if 'questions' not in st.session_state:
            st.session_state.questions = questions
            st.session_state.current_question = 0
            st.session_state.answers = {}

        if st.session_state.current_question < len(st.session_state.questions):
            question = st.session_state.questions[st.session_state.current_question]
            st.header(f"{question['question']}, Level is {question['level']}")
            answer = st.text_area("Please enter your answer", height=200)
            if st.button("Done"):
                st.session_state.answers[question["question"]] = answer
                st.session_state.current_question += 1
                st.experimental_rerun()
        else:
            clearing.empty()
            st.success("Done! Great job 👏🏼✨")
            # st.success("Checking the answers...")
            # scores = query_groq_answers_api(st.session_state.answers, st.session_state.questions)
            # # You can add code here to process the answers
            # st.write(st.session_state.answers)


else:
    st.warning("Please upload a resume to continue.")

