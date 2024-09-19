import streamlit as st
import requests
import json
import re

# function to extract_final_score
def extract_final_score(score_string):
    # Use a regular expression to find the final score in the string
    match = re.search(r'\s*Final Score:\s*\** (.*)', score_string)
    
    if match:
        score = match.group(1)
        
        # Check if the score is a fraction
        if '/' in score:
            numerator, denominator = map(float, score.split('/'))
            return numerator / denominator
        else:
            return float(score)
    else:
        raise ValueError("Final Score not found in the string.")
    



# Function to query the interview questions API
def query_groq_quest_api(resume, job_description):
    url = "http://localhost:5000/questions"
    headers = {"Content-Type": "application/json"}
    data = {
        "resume_details": resume,
        "job_description": job_description
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "The server response was not valid JSON."}
    else:
        return {"error": f"Request failed with status code {response.status_code}."}

# Function to get score from the API
def get_score(question, answer):
    url = "http://localhost:5000/score"
    headers = {"Content-Type": "application/json"}
    data = {
        "question": question,
        "response": answer
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError:
            return {"error": "The server response was not valid JSON."}
    else:
        return {"error": f"Request failed with status code {response.status_code}."}

# Streamlit page configuration for the interview page
st.set_page_config(page_title="Interview Questions")

st.title("Technical Interview")

# Retrieve resume and job description from session state
resume = st.session_state.get("resume", "")
job_description = st.session_state.get("job_description", "")

# Display error if resume or job description is missing
if not resume or not job_description:
    st.error("Resume or job description is missing! Please go back and upload.")
else:
  if st.session_state["match_percentage"]>=60:
    # Initialize questions if they are not already in session state
    if 'questions' not in st.session_state:
        st.header("Loading Questions...")
        
        # Call the function that queries the questions API
        qst = query_groq_quest_api(resume, job_description)
        
        # Use the response directly if it's already a dictionary
        questions_data = qst.get("response", {})
        
        # Access the questions directly from the structured JSON format
        questions = json.loads(questions_data) if isinstance(questions_data, str) else questions_data.get('Questions', [])
        
        # Debug output for questions
        print(f"This is the result of the match: {questions}")
        
        # Initialize session state for questions, current question, and answers
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
            <p style="font-size: 18px; color: black; ""><b>{question_text}</b> <span style="color: grey; font-size: 14px;">(Level: {question_level})</span></p>
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
            st.rerun()  # Rerun to update the next question displayed

    # If all questions are answered, show success message and send answers for scoring
    else:
        
        # Display all answers in a neatly formatted table
        st.markdown("### 📝 Your Answers and Scores")
        
        # Define a container with better formatting for the table structure
        table_style = """
        <style>
        .answer-box {
            text-align: left;
            padding: 10px;
            border-radius: 8px;
            background-color: #262730;
            color: #ffffff;
            margin-bottom: 20px;
            margin-top: 20px;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .answer-box .question {
            width: 40%;
            padding-right: 10px;
        }
        .answer-box .answer {
            width: 40%;
            padding-left: 10px;
        }
        .answer-box .score {
            width: 20%;
            text-align: center;
            padding: 10px;
            background-color: #1c1d21;
            border-radius: 8px;
        }
        </style>
        """
        
        # Add the table style to Streamlit
        st.markdown(table_style, unsafe_allow_html=True)
        final_score = 0
        # Iterate over the questions and answers
        for question, answer in st.session_state.answers.items():
            score_response = get_score(question, answer)
            # score = extract_final_score(score_response['response'])
            score = score_response['response']
            final_score = final_score + float(score)

            st.markdown(
                f"""
                <div class='answer-box'>
                    <div class='question'>
                        {question}
                    </div>
                    <div class='answer'>
                        {answer}
                    </div>
                    <div class='score'>
                        📊 {score}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        if final_score > 25: #the total score is 50
            st.success(f"""🎉 Done! Great job 👏🏼✨ this is your final score 🏆 {final_score}""")
            st.balloons()
        else:
            st.warning(f"""Unfortunately, your answers did not meet the criteria we are looking for at this time. 
                       Specifically, the evaluation highlighted areas where further alignment with our requirements and expectations is needed.
                       We encourage you to continue developing your skills and applying for future opportunities💪.
                       this is your final score  {final_score}""")
  else:
    st.warning(f"\n Unfortunately, You're not a match to this job description, you can find better 🥀 ")

