import json
import re

import fitz
import PyPDF2
from langchain_core.output_parsers import JsonOutputParser

from prompts.section_prompts import (
    ACHIEVEMENTS,
    CERTIFICATIONS,
    EDUCATIONS,
    EXPERIENCE,
    PROJECTS,
    SKILLS,
)
from structures.resume_structure import (
    Achievements,
    Certifications,
    Educations,
    Experiences,
    Projects,
    SkillSections,
)


def extract_text_from_pdf(pdf):
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_text(pdf: str):
    resume_text = ""

    pdf_reader = PyPDF2.PdfReader(pdf)
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

    return text


def parse_json_markdown(json_string: str) -> dict:
    try:
        # Try to find JSON string within first and last triple backticks
        if json_string[3:13].lower() == "typescript":
            json_string = json_string.replace(json_string[3:13], "", 1)

        if "JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA" in json_string:
            json_string = json_string.replace("JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA", "", 1)

        if json_string[3:7].lower() == "json":
            json_string = json_string.replace(json_string[3:7], "", 1)

        parser = JsonOutputParser()
        parsed = parser.parse(json_string)

        return parsed
    except Exception as e:
        print(e)
        return None


section_mapping = {
    "work_experience": {"prompt": EXPERIENCE, "schema": Experiences},
    "skill_section": {"prompt": SKILLS, "schema": SkillSections},
    "projects": {"prompt": PROJECTS, "schema": Projects},
    "education": {"prompt": EDUCATIONS, "schema": Educations},
    "certifications": {"prompt": CERTIFICATIONS, "schema": Certifications},
    "achievements": {"prompt": ACHIEVEMENTS, "schema": Achievements},
}


def write_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)