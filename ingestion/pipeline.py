import os
import io
from pypdf import PdfReader
from bs4 import BeautifulSoup
import requests
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

def ingest_emails(file_content: bytes, filename: str) -> list[Document]:
    # Placeholder for email parsing, normally involves email.parser
    # For now we'll do basic text extraction
    text = file_content.decode('utf-8', errors='ignore')
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk, metadata={"source": filename, "type": "email"}) for chunk in chunks]

def ingest_sds_tds_pdfs(file_content: bytes, filename: str) -> list[Document]:
    reader = PdfReader(io.BytesIO(file_content))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk, metadata={"source": filename, "type": "pdf"}) for chunk in chunks]

def ingest_website_content(url: str) -> list[Document]:
    response = requests.get(url, verify=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    for script_or_style in soup(['script', 'style']):
        script_or_style.decompose()
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
    
    split_chunks = text_splitter.split_text(cleaned_text)
    return [Document(page_content=c, metadata={"source": url, "type": "website"}) for c in split_chunks]
