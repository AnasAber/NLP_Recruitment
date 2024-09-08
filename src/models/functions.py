"""
In this file, we will have the main reasoning of our project.
- Functions
- model usage

"""
import os, sys, json
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from structures.job_structure import JobDetails
from structures.resume_structure import ResumeSchema
from prompts.resume_prompts import JOB_DETAILS_EXTRACTOR, TEXT_GENERATING_TEMPLATE, RESUME_DETAILS_EXTRACTOR, JSON_EXTRACTOR, GENERATING_QUESTIONS_TEMPLATE
from src.utils.config import section_mapping, write_json
from src.models.models import groq_query


# Utility functions
def get_resume_details(resume_text: str=None):
    """
    Extracts user data from the given file content.

    Args:
        resume_file (str): the user data content.

    Returns:
        dict: The extracted user data in JSON format.
    """
    print("\nGetting user data...")

    try:
        if resume_text:
            print("I'm in get_resume_details")
            json_parser = JsonOutputParser(pydantic_object=ResumeSchema)

            prompt = PromptTemplate(
                template=RESUME_DETAILS_EXTRACTOR,
                input_variables=["resume_text"],
                partial_variables={"format_instructions": json_parser.get_format_instructions()}
                ).format(resume_text=resume_text)
            
            print("I'm about to query")
            response_json = groq_query(prompt=prompt)

            # resume_details = resume_to_json(resume_text)
            print(f"this is the response of the resume details to json:\
            {response_json}")
            return response_json
    except Exception as e:
        raise Exception("Invalid file format. Please provide a PDF.")
        




def get_job_details(job_site_content: str):
    """
    Extracts job details from the specified job content.

    Args:
        job_site_content (str): The content of the job posting.

    Returns:
        dict: A dictionary containing the extracted job details.
    """
    
    print("\nExtracting job details...")

    try:
        if job_site_content:
            json_parser = JsonOutputParser(pydantic_object=JobDetails)
            
            prompt = PromptTemplate(
                template=JOB_DETAILS_EXTRACTOR,
                input_variables=["job_description"],
                partial_variables={"format_instructions": json_parser.get_format_instructions()}
                ).format(job_description=job_site_content)

            job_details = groq_query(prompt)
            if job_details:
                print("job details compelete!")
                print(f"this is the response of the job details to json:\
                {job_details}")
                return job_details
            else:
                print("there's some error in job extraction")
    except Exception as e:
        raise Exception("An error occurred while extracting job details! Check the groq api.")



def json_extractor(text: str):
    print("\nFormatting the JSON strings...")
    try:

        prompt = PromptTemplate(
            template=JSON_EXTRACTOR,
            input_variables=["text"],
            ).format(text=text)

        jsonn = groq_query(prompt=prompt)
        return jsonn
    
    except Exception as e:
        raise Exception("An error occurred while calculating the matching score!")





def get_matching_score(job_details: str, resume_text: str):
    """
    Calculate the similarity scores between the resume and job details.

    Args:
        job_details (str): The extracted job details.
        user_data (str): The extracted user data.

    Returns:
        float: The matching score between the resume and job details.
    """
       
    # job_details = json_extractor(job_details)
    # resume_text = json_extractor(resume_text)

    # print({job_details})

    # job_details = json.loads(job_details)
    # resume_text = json.loads(resume_text)

    print("\nCalculating matching score...")
    try:

        prompt = PromptTemplate(
            template=TEXT_GENERATING_TEMPLATE,
            input_variables=["resume", "job_description"],
            ).format(resume=resume_text, job_description=job_details)

        scores = groq_query(prompt=prompt)
        print(f"this is the score response: \n{scores}")
        return scores

    except Exception as e:
        raise Exception("An error occurred while calculating the matching score!")




def generate_questions(resume_details, job_desc):

    print("\nGenerating questions...")
    try:
        print(f" this is the value of job_desc: \n{job_desc}\n")
        print(f" this is the value of resume_details: \n{resume_details}")
        resume_details = get_resume_details(resume_details)

        prompt = PromptTemplate(
            template=GENERATING_QUESTIONS_TEMPLATE,
            input_variables=["job_description", "candidate_resume_infos"],
            ).format(job_description=job_desc, candidate_resume=resume_details)

        questions = groq_query(prompt=prompt)
        print(f"these are the questions response: \n{questions}")
        return questions

    except Exception as e:
        raise Exception("An error occurred while generating the questions!")



def get_answers_score(answers, questions):
    """
    Get the score of candidate answers.

    Args:
        answers (dict): The answers of the candidates.
        questions (dict): The questions the candidate answered.
    """
    
    print("\nRate Questions...")
    # try:

        # prompt = PromptTemplate(
        #     template=RATE_QUESTIONS_TEMPLATE,
        #     input_variables=["questions", "answers"],
        #     ).format(questions=questions, answers=answers)

        # ratings = groq_query(prompt=prompt)
        # print(f"these are the ratings response: \n{ratings}")
        # return ratings

    # except Exception as e:
    #     raise Exception("An error occurred while rating the questions!")






def resume_details_builder(job_details: dict, user_data: dict):
    """
    Builds a resume based on the provided job details and user data.

    Args:
        job_details (dict): A dictionary containing the job description.
        user_data (dict): A dictionary containing the user's resume or work information.

    Returns:
        dict: The generated resume details in JSON.

    Raises:
        FileNotFoundError: If the system prompt files are not found.
    """
    try:

        resume_details = dict()

        # Personal Information Section
        resume_details["personal"] = { 
            "name": user_data["name"], 
            "phone": user_data["phone"], 
            "email": user_data["email"],
            "github": user_data["media"]["github"], 
            "linkedin": user_data["media"]["linkedin"]
            }
        st.markdown("**Personal Info Section**")
        st.write(resume_details)

        # Other Sections
        for section in ['work_experience', 'projects', 'skill_section', 'education', 'certifications', 'achievements']:
            section_log = f"Processing Resume's {section.upper()} Section..."

            json_parser = JsonOutputParser(pydantic_object=section_mapping[section]["schema"])
            
            prompt = PromptTemplate(
                template=section_mapping[section]["prompt"],
                partial_variables={"format_instructions": json_parser.get_format_instructions()}
                ).format(section_data = json.dumps(user_data[section]), job_description = json.dumps(job_details))

            response = groq_query(prompt=prompt)

            # Check for empty sections
            if response is not None and isinstance(response, dict):
                if section in response:
                    if response[section]:
                        if section == "skill_section":
                            resume_details[section] = [i for i in response['skill_section'] if len(i['skills'])]
                        else:
                            resume_details[section] = response[section]
            
            st.markdown(f"**{section.upper()} Section**")
            st.write(response)

        resume_details['keywords'] = ', '.join(job_details['keywords'])
        

        write_json(resume_details)
        # st.write(f"resume_path: {resume_path}")
        st.write("Resume Details Generated Successfully!")
        return resume_details
    except Exception as e:
        print(e)
        st.write("Error: \n\n",e)
        return resume_details
    



# def get_relevant_skills(candidate_embeddings, job_embeddings, top_n=5):
#     """
#     Compute the similarity between candidate skills and job requirements using cosine similarity
#     and return the top N relevant skills.
#     """
#     similarities = np.dot(candidate_embeddings, job_embeddings.T)
#     top_indices = np.argsort(similarities)[-top_n:]
#     return top_indices

# # Main functions

# def generate_personalized_questions(candidate_data, job_description):
#     """
#     Generate personalized questions for a candidate based on their data and job description.
#     """
#     candidate_skills = candidate_data.get("skills", [])
#     job_requirements = job_description.get("requirements", [])

#     # Generate embeddings for skills and requirements
#     candidate_embeddings = generate_embeddings(candidate_skills)
#     job_embeddings = generate_embeddings(job_requirements)

#     # Find relevant skills
#     relevant_skills_indices = get_relevant_skills(candidate_embeddings, job_embeddings)
#     relevant_skills = [candidate_skills[i] for i in relevant_skills_indices]

#     # Generate questions
#     questions = []
#     for skill in relevant_skills:
#         prompt = generate_prompt(skill, job_requirements)
#         question = generate_question(prompt)
#         questions.append(question)
    
#     return questions
