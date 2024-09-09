import streamlit as st
import requests, json, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import extract_text


def query_groq_api(resume, job_description):
    url = "http://localhost:5000/query"
    headers = {"Content-Type": "application/json"}
    data = {"resume": resume, "job_description": job_description}
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
    
st.set_page_config(page_title="Job hunting assistant")

st.title("Resume Matching System")

st.write("Upload your resume and job description to get the matching percentage.")

uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
job_description = st.text_area("Job Description", height=200)
button = st.button("Process Resume")


if button and uploaded_resume and job_description:
    clearing = st.empty()

    # Read and encode the resume only if a file is uploaded
    resume = extract_text(uploaded_resume)
    with st.spinner("Processing..."):
        results = query_groq_api(resume, job_description)

        print(f"this is the result of the match: \
              {results}\
              ")
        
        result = json.loads(results["response"])

        if "error" in result:
            st.error(result["error"])
        else:

            # Use columns for better organization
            col1, col2 = st.columns(2)

            # Match percentage section with a progress bar
            with col1:
                st.header("Match Percentage")
                match_percentage = result['Match Percentage']
                st.progress(match_percentage / 100)  # Progress bar
                if result["Match Percentage"]< 60:
                    st.write(
                        f"\n Unfortunately, You're not a match to this job description, you can find better 🥀 %"
                    )
                else:
                    scores = f"Your resume matches the job description with a score of {result['Match Percentage']}"
                    st.write(
                    f"**Your resume matches the job description with a score of `{match_percentage}%`**"
                    )

                    # Extracted entities section
                    st.header("Extracted Entities")
                    st.markdown("### **Experience**")
                    st.write(result["Extracted Entities"]["Experience"])

                    st.markdown("### **Competence**")
                    st.write(result["Extracted Entities"]["Competence"])

                    st.markdown("### **Qualifications**")
                    st.write(result["Extracted Entities"]["Qualifications"])

                    # Missing keywords/skills section with a warning indicator
                    st.header("Missing Keywords/Skills")
                    if result["Missing Keywords/Skills"]:
                        st.warning("Some keywords or skills are missing!")
                        st.write(result["Missing Keywords/Skills"])
                    else:
                        st.success("No missing keywords or skills!")

                    # Final thoughts section with styling
                    st.header("Final Thoughts")
                    st.info(result["Final Thoughts"])


                    st.header("Loading Questions...")

                    # Call the function that queries the questions API
                    qst = query_groq_quest_api(resume, job_description)

                    # Use the response directly if it's already a dictionary
                    questions_data = qst.get("response", {})

                    # Access the questions directly from the structured JSON format
                    questions = json.loads(questions_data) if isinstance(questions_data, str) else questions_data.get('Questions', [])

                    # Debug output for questions
                    print(f"This is the result of the match: {questions}")

                    # Clear any previous content
                    clearing.empty()

                    # Initialize session state for questions, current question, and answers
                    if 'questions' not in st.session_state:
                        st.session_state.questions = questions
                        st.session_state.current_question = 0
                        st.session_state.answers = {}

                    # If there are remaining questions, display the current question
                    if st.session_state.current_question < len(st.session_state.questions):
                        current_question = st.session_state.questions[st.session_state.current_question]
                        question_text = current_question.get('Question', 'No question available')
                        question_level = current_question.get('Level', 'N/A')

                        # Display question in a card-like format
                        st.markdown(f"""
                        <div style="padding: 20px; border-radius: 10px; background-color: #f9f9f9; border: 1px solid #ddd;">
                            <h4 style="color: #333;">📝 <b>Question {st.session_state.current_question + 1}:</b></h4>
                            <p style="font-size: 18px;"><b>{question_text}</b> <span style="color: grey; font-size: 14px;">(Level: {question_level})</span></p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Text area for user to write their answer
                        answer = st.text_area("💡 Your Answer", height=200)

                        # Create a progress bar for visual progress
                        st.progress((st.session_state.current_question + 1) / len(st.session_state.questions))

                        # Submit button with icon
                        if st.button("✅ Submit Answer"):
                            st.session_state.answers[question_text] = answer
                            st.session_state.current_question += 1
                            st.experimental_rerun()  # Rerun to update the next question displayed

                    # If all questions are answered, show success message
                    else:
                        st.success("🎉 Done! Great job 👏🏼✨")
                        st.balloons()

                        # Display all answers in a neatly formatted table
                        st.markdown("### 📝 Your Answers")
                        for question, answer in st.session_state.answers.items():
                            st.markdown(f"**{question}**: {answer}")

            # # Clear any unnecessary elements
            # clearing.empty()

            
            # # Optional: Display all answers collected so far for debugging
            # if st.session_state.answers:
            #     st.write("Your answers so far:")
            #     for question, answer in st.session_state.answers.items():
            #         st.write(f"{question}: {answer}")

            # st.success("Checking the answers...")
            # scores = query_groq_answers_api(st.session_state.answers, st.session_state.questions)
            # # You can add code here to process the answers
            # st.write(st.session_state.answers)


else:
    st.warning("Please upload a resume to continue.")
