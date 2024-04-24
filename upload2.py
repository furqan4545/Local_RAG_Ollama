import PyPDF2
import re
import json
import pandas as pd
from docx import Document

# Function to read and process PDF files
def process_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ' '.join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
    return text

# Function to read and process text files
def process_text(file_path):
    with open(file_path, 'r', encoding="utf-8") as txt_file:
        text = txt_file.read()
    return text

def extract_text_from_json(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'text' and isinstance(value, str):
                yield value
            else:
                yield from extract_text_from_json(value)
    elif isinstance(data, list):
        for item in data:
            yield from extract_text_from_json(item)

# Function to read and process JSON files
# def process_json(file_path):
#     with open(file_path, 'r', encoding="utf-8") as json_file:
#         data = json.load(json_file)
#         text = json.dumps(data, ensure_ascii=False)
#     return text

def process_json(file_path):
    with open(file_path, 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        text = ' '.join(extract_text_from_json(data))
    return text

# Function to read and process DOCX files
def process_docx(file_path):
    doc = Document(file_path)
    text = ' '.join([paragraph.text for paragraph in doc.paragraphs if paragraph.text])
    return text

# Function to read and process CSV files
def process_csv(file_path):
    df = pd.read_csv(file_path)
    text = ' '.join(df.apply(lambda row: ' '.join(row.astype(str)), axis=1))
    return text

# Function to normalize and chunk text
def normalize_and_chunk_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < 1000:
            current_chunk += (sentence + " ").strip()
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# Function to process a list of files
def process_files(file_paths):
    for file_path in file_paths:
        extension = file_path.split('.')[-1].lower()
        if extension == 'pdf':
            text = process_pdf(file_path)
        elif extension == 'txt':
            text = process_text(file_path)
        elif extension == 'json':
            text = process_json(file_path)
        elif extension == 'docx':
            text = process_docx(file_path)
        elif extension == 'csv':
            text = process_csv(file_path)
        else:
            continue
        chunks = normalize_and_chunk_text(text)
        with open("vault_custom.txt", "a", encoding="utf-8") as vault_file:
            for chunk in chunks:
                vault_file.write(chunk.strip() + "\n\n")



############## Example usage ##############
# file_paths = ['example.pdf', 'example.txt', 'data.json', 'document.docx', 'data.csv']
file_paths = ['rag.pdf', 'speech.json', 'attention_paper.pdf']
process_files(file_paths)
