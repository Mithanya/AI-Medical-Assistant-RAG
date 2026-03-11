"""
data_loader.py
---------------
Load medical documents (PDF/TXT) and split them into chunks for RAG engine.
"""

import os
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2

def load_pdf(file_path: str) -> str:
    """Load PDF content as text."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def load_txt(file_path: str) -> str:
    """Load TXT file content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def load_and_split(data_dir: str) -> List[Document]:
    """
    Load all PDFs and TXTs from a directory and split them into chunks.
    Returns a list of LangChain Document objects.
    """
    documents = []
    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        if file_name.lower().endswith(".pdf"):
            text = load_pdf(file_path)
        elif file_name.lower().endswith(".txt"):
            text = load_txt(file_path)
        else:
            continue

        if text.strip():
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = splitter.split_text(text)
            for chunk in chunks:
                documents.append(
                    Document(page_content=chunk, metadata={"source": file_name})
                )
    return documents