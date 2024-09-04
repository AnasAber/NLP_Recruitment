from langchain_core.output_parsers import JsonOutputParser
from prompts.section_prompts import EXPERIENCE, SKILLS, PROJECTS, EDUCATIONS, CERTIFICATIONS, ACHIEVEMENTS
from structures.resume_structure import Experiences, SkillSections, Projects, Educations, Certifications, Achievements
import json
import base64
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import fitz  # PyMuPDF
import PyPDF2
import re


def extract_text_from_pdf(pdf):
    doc = fitz.open(stream=pdf.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_pdf_text(pdf_file):
    """
    Extracts text from a PDF file using LangChain.
    
    Args:
        pdf_file (str): Path to the PDF file.
        
    Returns:
        str: Text extracted from the PDF file.
    """
    # Load the PDF file
    loader = PyPDFLoader(pdf_file)
    documents = loader.load()
    
    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # Combine the text chunks into a single string
    text = "\n\n".join([t.page_content for t in texts])


def extract_text(pdf: str):
    resume_text = ""

    pdf_reader = PyPDF2.PdfReader(pdf)
    num_pages = len(pdf_reader.pages)

    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text().split("\n")

        # Remove Unicode characters from each line
        cleaned_text = [re.sub(r'[^\x00-\x7F]+', '', line) for line in text]

        # Join the lines into a single string
        cleaned_text_string = '\n'.join(cleaned_text)
        resume_text += cleaned_text_string
        
        return resume_text
    
    return text
def save_pdf(file, save_directory):
    """
    Saves the uploaded PDF file to the specified directory with the name format 'output_{name_of_pdf}.pdf'.

    :param file: File object (e.g., from an upload)
    :param save_directory: The directory where the file should be saved
    :return: Path where the file is saved
    """
    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Get the original filename and create the output filename
    original_filename = file.filename
    file_name_without_extension = os.path.splitext(original_filename)[0]
    output_filename = f"output_{file_name_without_extension}.pdf"
    print(output_filename)
    
    # Construct the full path for saving the file
    output_path = os.path.join(save_directory, output_filename)

    # Save the file to the specified directory
    with open(output_path, "wb") as f:
        f.write(file.read())





def parse_json_markdown(json_string: str) -> dict:
    try:
        # Try to find JSON string within first and last triple backticks
        if json_string[3:13].lower() == "typescript":
            json_string = json_string.replace(json_string[3:13], "",1)
        
        if 'JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA' in json_string:
            json_string = json_string.replace("JSON_OUTPUT_ACCORDING_TO_RESUME_DATA_SCHEMA", "",1)
        
        if json_string[3:7].lower() == "json":
            json_string = json_string.replace(json_string[3:7], "",1)
    
        parser = JsonOutputParser()
        parsed = parser.parse(json_string)

        return parsed
    except Exception as e:
        print(e)
        return None
    
section_mapping = {
    "work_experience": {"prompt":EXPERIENCE, "schema": Experiences},
    "skill_section": {"prompt":SKILLS, "schema": SkillSections},
    "projects": {"prompt":PROJECTS, "schema": Projects},
    "education": {"prompt":EDUCATIONS, "schema": Educations},
    "certifications": {"prompt":CERTIFICATIONS, "schema": Certifications},
    "achievements": {"prompt":ACHIEVEMENTS, "schema": Achievements},
}


def write_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)



# import re
# import json
# import math
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics import pairwise


# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
# from nltk.tokenize import word_tokenize
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('punkt')

# def key_value_chunking(data, prefix=""):
#     """Chunk a dictionary or list into key-value pairs.

#     Args:
#         data (dict or list): The data to chunk.
#         prefix (str, optional): The prefix to use for the keys. Defaults to "".

#     Returns:
#         A list of strings representing the chunked key-value pairs.
#     """
#     chunks = []
#     stop_needed = lambda value: '.' if not isinstance(value, (str, int, float, bool, list)) else ''
    
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if value is not None:
#                 chunks.extend(key_value_chunking(value, prefix=f"{prefix}{key}{stop_needed(value)}"))
#     elif isinstance(data, list):
#         for index, value in enumerate(data):
#             if value is not None:
#                 chunks.extend(key_value_chunking(value, prefix=f"{prefix}_{index}{stop_needed(value)}"))
#     else:
#         if data is not None:
#             chunks.append(f"{prefix}: {data}")
    
#     return chunks
    

# def overlap_coefficient(document1: str, document2: str) -> float:
#     """Calculate the overlap coefficient between two documents.

#     The overlap coefficient is a measure of the overlap between two sets, 
#     and is defined as the size of the intersection divided by the smaller 
#     of the size of the two sets.

#     Args:
#         document1 (str): The first document.
#         document2 (str): The second document.

#     Returns:
#         float: The overlap coefficient between the two documents.
#     """    
#     # List the unique words in a document
#     words_in_document1 = set(normalize_text(document1))
#     words_in_document2 = set(normalize_text(document2))

#     # Find the intersection of words list of document1 & document2
#     intersection = words_in_document1.intersection(words_in_document2)

#     # Calculate overlap coefficient
#     try:
#         overlap_coefficient = float(len(intersection)) / min(len(words_in_document1), len(words_in_document2))
#     except ZeroDivisionError:
#         overlap_coefficient = 0.0

#     return overlap_coefficient
    
# def jaccard_similarity(document1: str, document2: str) -> float:
#     """Calculate the Jaccard similarity between two documents.

#     The Jaccard similarity is a measure of the similarity between two sets, 
#     and is defined as the size of the intersection divided by the size of 
#     the union of the two sets.

#     Args:
#         document1 (str): The first document.
#         document2 (str): The second document.

#     Returns:
#         float: The Jaccard similarity between the two documents.
#     """    
#     # List the unique words in a document
#     words_in_document1 = set(normalize_text(document1))
#     words_in_document2 = set(normalize_text(document2))

#     # Find the intersection of words list of document1 & document2
#     intersection = words_in_document1.intersection(words_in_document2)

#     # Find the union of words list of document1 & document2
#     union = words_in_document1.union(words_in_document2)
        
#     # Calculate Jaccard similarity score 
#     try:
#         jaccard_similarity = float(len(intersection)) / len(union)
#     except ZeroDivisionError:
#         jaccard_similarity = 0.0

#     return jaccard_similarity

# def cosine_similarity(document1: str, document2: str) -> float:
#     """Calculate the cosine similarity between two documents.

#     Args:
#         document1 (str): The first document.
#         document2 (str): The second document.

#     Returns:
#         float: The cosine similarity between the two documents.
#     """
#     # Create a TF-IDF vectorizer
#     vectorizer = TfidfVectorizer()

#     # Transform the documents into TF-IDF vectors
#     vectors = vectorizer.fit_transform([document1, document2])

#     cosine_similarity_score = pairwise.cosine_similarity(vectors[0], vectors[1])
#     # Calculate the cosine similarity between the two vectors
#     # cosine_similarity = np.dot(vectors[0], vectors[1].T) / (np.linalg.norm(vectors[0].toarray()) * np.linalg.norm(vectors[1].toarray()))

#     return cosine_similarity_score.item()



# def normalize_text(text: str) -> list:
#     """Normalize the input text.

#     This function tokenizes the text, removes stopwords and punctuations, 
#     and applies stemming.

#     Args:
#         text (str): The text to normalize.

#     Returns:
#         list: The list of normalized words.
#     """    
#     # Step 1: Tokenization
#     words = word_tokenize(text)

#     # Step 2: Data Cleaning - Remove Stopwords and Punctuations 
#     words = [re.sub('[^a-zA-Z]', '', word).lower() for word in words]

#     # Step 3: Remove empty tokens
#     words = [word for word in words if len(word)] 

#     # Step 4: Remove Stopwords
#     stop_words = set(stopwords.words('english'))
#     words = [word for word in words if word not in stop_words]

#     # Step 5: Stemming
#     stemmer = PorterStemmer()
#     words = [stemmer.stem(word) for word in words]

#     #STEP 3 : LEMMATIZATION
#     # lemmatizer=WordNetLemmatizer()
#     # words=[lemmatizer.lemmatize(word) for word in words]
    
#     return words 