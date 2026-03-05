from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
from ingestion.pipeline import ingest_sds_tds_pdfs, ingest_emails, ingest_website_content

router = APIRouter()

@router.post("/upload")
async def upload_knowledgebase_files(
    files: List[UploadFile] = File(...),
    document_type: str = Form(..., description="Type of document, e.g., 'SDS', 'TDS', 'EMAIL'")
):
    """
    Admin route to upload files (SDS/TDS PDFs, exported emails) for the knowledgebase.
    """
    allowed_extensions = {".json", ".pdf", ".txt", ".csv", ".docx"}
    total_chunks = 0
    for file in files:
        ext = ""
        if "." in file.filename:
            ext = "." + file.filename.rsplit(".", 1)[-1].lower()
            
        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail=f"File {file.filename} has an unsupported extension. Allowed: {', '.join(allowed_extensions)}")
            
        content = await file.read()
        if document_type.upper() in ["SDS", "TDS"] or file.filename.endswith(".pdf"):
            docs = ingest_sds_tds_pdfs(content, file.filename)
        elif document_type.upper() == "EMAIL":
            docs = ingest_emails(content, file.filename)
        else:
            # Fallback
            docs = ingest_emails(content, file.filename)
        
        # Here we would normally insert chunks into Chroma engine
        from chatbot.engine import chatbot_engine
        chatbot_engine.add_documents(docs)
        total_chunks += len(docs)
        
    return {"message": f"Successfully processed {len(files)} files into {total_chunks} vector chunks."}

@router.post("/scrape")
async def scrape_website(url: str):
    """
    Admin route to ingest website content by providing a URL.
    """
    try:
        docs = ingest_website_content(url)
        from chatbot.engine import chatbot_engine
        chatbot_engine.add_documents(docs)
        return {"message": f"Successfully scraped {url} into {len(docs)} chunks."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
