# document_handler.py

import os
import PyPDF2

UPLOADS_DIR = "uploads"

def get_latest_uploaded_file():
    """
    Returns the path to the most recent file in the uploads folder.
    """
    files = [os.path.join(UPLOADS_DIR, f) for f in os.listdir(UPLOADS_DIR)
             if os.path.isfile(os.path.join(UPLOADS_DIR, f))]
    if not files:
        raise FileNotFoundError(f"No files found in {UPLOADS_DIR}. Please upload a PDF or TXT.")
    latest_file = max(files, key=os.path.getctime)
    if os.path.getsize(latest_file) == 0:
        raise ValueError(f"The file '{latest_file}' is empty. Please upload a valid file.")
    return latest_file

def read_uploaded_file():
    """
    Reads text from the most recent file in uploads.
    Supports PDF and TXT files.
    """
    file_path = get_latest_uploaded_file()
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return read_pdf(file_path)
    elif ext == ".txt":
        return read_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Only PDF and TXT are allowed.")

def read_pdf(file_path):
    """
    Reads all text from a PDF file safely.
    """
    text = ""
    with open(file_path, "rb") as f:
        try:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                raise ValueError(f"PDF '{file_path}' has no pages.")
            for page in reader.pages:
                page_text = page.extract_text() or ""
                text += page_text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {e}")
    if not text.strip():
        raise ValueError(f"PDF '{file_path}' could not be read or is empty.")
    return text

def read_txt(file_path):
    """
    Reads plain text file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    if not text.strip():
        raise ValueError(f"Text file '{file_path}' is empty.")
    return text
