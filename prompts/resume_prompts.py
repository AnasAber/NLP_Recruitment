TEXT_GENERATING_TEMPLATE = """
You are a skilled ATS (Application Tracking System) scanner with deep knowledge of Data Science, Web Development, Big Data Engineering, DevOps, Data Analysis, and a thorough understanding of ATS functionality. Your task is to perform the following tasks:

1. Extract key entities from the provided resume JSON text description, including Experience, Competence, and Qualifications.
2. Evaluate the resume against the job JSON text description and provide a match percentage.
3. Recognize related technologies and frameworks:
   - For example, if a candidate lists "Spring," they likely have knowledge of Java EE (J2EE).
   - If a candidate lists "Java," they might be familiar with other Java-related technologies such as J2EE or frameworks like Spring and Hibernate.
   - recognize that TensorFlow is related to machine learning.
4. Identify missing keywords or skills that are present in the job description but not in the resume.
5. Provide any additional insights or thoughts on the candidate's suitability for the position.

**Resume:**
{resume}

**Job Description:**
{job_description}

Your output should be structured in a JSON file, as follows:
- Extracted Entities:
  - Experience: [Extracted Experience]
  - Competence: [Extracted Competence]
  - Qualifications: [Extracted Qualifications]
- Match Percentage: [Percentage]
- Missing Keywords/Skills: [List of Keywords/Skills]
- Final Thoughts: [Your Insights]

No brief explanaition, no introductions such as "Here is the output in the required JSON format:", No extra text or talking, return the JSON format as it is.


Use your expertise to make this evaluation as accurate as possible.
"""




GENERATING_QUESTIONS_TEMPLATE = """
You are a skilled interviewer with deep knowledge of the job market and requirements. Your task is to generate a set of questions to assess the candidate's suitability for the job.

**Job Description:**
{job_description}

**Candidate Information:**
{candidate_resume}
<task>
Generate a set of questions that will help evaluate the candidate's experience, skills, and qualifications for the job. The questions should be specific, relevant, and challenging.
Generate 10 questions with a mix of levels, to test the candidate's level.
<task>


Your output should be a list of questions in the following JSON format:
[
  {
    "question": "Question 1",
    "level": "Whether it's an easy question, medium, or hard"
  },
  {
    "question": "Question 2",
    "level": "Whether it's an easy question, medium, or hard"
  },
  ...
]

for example:
[
  {
    "question": "What are the benefits of Generative AI?",
    "level": "easy"
  },
  {
    "question": "Can you explain the ethical implications of AI?",
    "level": "medium"
  },
  {
    "question": "How would you optimize a large language model for performance?",
    "level": "hard"
  }
]


No brief explaination, no introductions such as "Here is the output in the required JSON format:", No extra text or talking, return the JSON format as it is.

Use your expertise to make these questions as relevant and effective as possible.
"""


# RATE_QUESTIONS_TEMPLATE= """


# """


RESUME_DETAILS_EXTRACTOR = """<objective>
Parse a text-formatted resume efficiently and extract diverse applicant's data into a structured JSON format.
</objective>

<input>
The following text is the applicant's resume in plain text format:

{resume_text}
</input>

<instructions>
Follow these steps to extract and structure the resume information:

1. Analyze Structure:
   - Examine the text-formatted resume to identify key sections (e.g., personal information, education, experience, skills, certifications).
   - Note any unique formatting or organization within the resume.

2. Extract Information:
   - Systematically parse each section, extracting relevant details.
   - Pay attention to dates, titles, organizations, and descriptions.

3. Handle Variations:
   - Account for different resume styles, formats, and section orders.
   - Adapt the extraction process to accurately capture data from various layouts.

5. Optimize Output:
   - Handle missing or incomplete information appropriately (use null values or empty arrays/objects as needed).
   - Standardize date formats, if applicable.

6. Validate:
   - Review the extracted data for consistency and completeness.
   - Ensure all required fields are populated if the information is available in the resume.
</instructions>

Remember, you will return a JSON format, so no comments or introductions as they will affect the quality of the JSON format.

{format_instructions}"""



JSON_EXTRACTOR = """
You are a skilled expert in python and JSON formatting.
<task>
Identify the JSON text from a given string, delete the access text to make it a valid JSON format, and return the correct, valid JSON format.
</task>

{text}
"""



JOB_DETAILS_EXTRACTOR = """
<task>
Identify the key details from a job description and company overview to create a structured JSON output. Focus on extracting the most crucial and concise information that would be most relevant for tailoring a resume to this specific job.
</task>

<job_description>
{job_description}
</job_description>

Note: The "keywords", "job_duties_and_responsibilities", and "required_qualifications" sections are particularly important for resume tailoring. Ensure these are as comprehensive and accurate as possible.

No brief explanaition, no introductions such as "Here is the JSON output based on the provided job description and company overview:", No extra text or talking, return the JSON format as it is.

{format_instructions}
"""