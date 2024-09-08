"""
Here you'll find the functions responsible for pre-processing the data

"""

import re

import PyPDF2
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from prompts.resume_prompts import (
    JOB_DETAILS_EXTRACTOR,
    RESUME_DETAILS_EXTRACTOR,
    TEXT_GENERATING_TEMPLATE,
)
from src.models.models import groq_query
from structures.resume_structure import ResumeSchema


def extract_text_from_pdf(pdf_path: str):
    resume_text = ""

    with open(pdf_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text().split("\n")

            # Remove Unicode characters from each line
            cleaned_text = [re.sub(r"[^\x00-\x7F]+", "", line) for line in text]

            # Join the lines into a single string
            cleaned_text_string = "\n".join(cleaned_text)
            resume_text += cleaned_text_string

        return resume_text


def resume_to_json(self, resume_text):
    """
    Converts a resume in PDF format to JSON format.

    Args:
        resume_text (str): The extracted resume text.

    Returns:
        dict: The resume data in JSON format.
    """

    json_parser = JsonOutputParser(pydantic_object=ResumeSchema)
    print("I'm in Resume to json")

    prompt = PromptTemplate(
        template=RESUME_DETAILS_EXTRACTOR,
        input_variables=["resume_text"],
        partial_variables={"format_instructions": json_parser.get_format_instructions()},
    ).format(resume_text=resume_text)

    print("I'm hedding out in Resume to json")

    response_json = groq_query(prompt=prompt)

    print(
        f"this is the response of the resume to json:\
              {response_json}"
    )

    return response_json
