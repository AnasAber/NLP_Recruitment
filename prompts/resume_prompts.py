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

**Resume:**
{resume}

**Job Description:**
{job_description}

Your output should be structured in a JSON format, as follows:
- Questions:
  - Question: [First generated question]
    - Level: [Whether it's an easy question, medium, or hard]
  - Question: [Second generated question]
    - Level: [Whether it's an easy question, medium, or hard]
  - ...
  - Question: [Tenth generated question]
    - Level: [Whether it's an easy question, medium, or hard]

No brief explanation, no introductions such as "Here is the output in the required JSON format:", no extra text or talking, return the JSON format as it is.

Use your expertise to make these questions as relevant and effective as possible.
"""



RATE_ANSWERS_TEMPLATE = """
You are skilled in evaluating interview responses. You will assess candidates' answers to interview questions, ensuring consistency and fairness in the evaluation process.

For each question, please use the following criteria to evaluate the candidate's response:

Question:
{question}

Candidate's Answer:
{answer}

Evaluation Criteria:

1. Relevance:
   - Description: How well does the answer address the question asked? Is it on-topic and pertinent to the question?
   - Rating:  (0-1)
     - 1 Excellent: Demonstrates a keen understanding of the concept or subject. The response is well thought-out, complete, and addresses all aspects of the question without requiring probing or follow-up.
     - 0.75 Good: Shows a clear understanding of the concept. The response is complete and well-articulated but may not be as thorough as an excellent response. Some potential for improvement is evident.
     - 0.5 Adequate: Provides an adequate understanding but may miss some key points. The response is not as in-depth and might require some probing or follow-up.
     - 0.25 Poor: Shows limited understanding of the concept. The response may be vague, incomplete, or off-topic, requiring extensive probing or follow-up.
     - 0 Inadequate: Fails to answer the question or provides an unacceptable response. The response does not convey the required level of experience or expertise.

2. Completeness:
   - Description: Does the answer cover all aspects of the question? Are there any significant omissions or gaps?
   - Rating: (0-1)
     - 1 Excellent: Thoroughly covers all aspects of the question without omissions.
     - 0.75 Good: Covers most aspects of the question with minor omissions.
     - 0.5 Adequate: Covers the question but has notable gaps or omissions.
     - 0.25 Poor: The response is incomplete and lacks significant parts of the question.
     - 0 Inadequate: The response does not address the question or is highly incomplete.

3. Clarity:
   - Description: How clear and understandable is the answer? Is the response well-organized and easy to follow?
   - Rating: (0-1)
     - 1 Excellent: The response is very clear, well-organized, and easy to follow.
     - 0.75 Good: The response is clear and organized but may have minor readability issues.
     - 0.5 Adequate: The response is understandable but may have organization or clarity issues.
     - 0.25 Poor: The response is unclear or disorganized, making it hard to understand.
     - 0 Inadequate: The response is very unclear or chaotic, making it difficult to follow.

4. Technical Accuracy:
   - Description: Is the technical content of the answer correct? Are there any factual errors or misconceptions?
   - Rating: (0-1)
     - 1 Excellent: The response is technically accurate with no errors or misconceptions.
     - 0.75 Good: Mostly accurate with minor errors or misconceptions.
     - 0.5 Adequate: Generally accurate but contains significant errors or misconceptions.
     - 0.25 Poor: Inaccurate with several errors or misconceptions.
     - 0 Inadequate: Fundamentally flawed with poor technical grasp.

5. Creativity and Insight:
   - Description: Does the answer demonstrate creativity or provide unique insights? How well does it show problem-solving ability or innovation?
   - Rating: (0-1)
     - 1 Excellent: Demonstrates exceptional creativity or unique insights, showing strong problem-solving abilities.
     - 0.75 Good: Shows creativity or insight and a good level of problem-solving ability.
     - 0.5 Adequate: Displays some creativity or insight but is fairly standard in approach.
     - 0.25 Poor: Shows limited creativity or insight, with a conventional approach.
     - 0 Inadequate: Lacks creativity or insight, with a very standard or uninspired response.

Final Note Calculation:
To calculate the final score, sum the ratings for each criterion. Please don't return the details; just provide the final score.

*Final Score:* (0-5) 
"""












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


# JSON_EXTRACTOR = """
# You are a skilled expert in python and JSON formatting.
# <task>
# Identify the JSON text from a given string, delete the access text to make it a valid JSON format, and return the correct, valid JSON format.
# </task>

# {text}
# """



