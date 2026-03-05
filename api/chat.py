from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from chatbot.engine import chatbot_engine

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class FAQRequest(BaseModel):
    limit: int = 10

@router.post("/ask")
async def ask_question(request: ChatRequest):
    """
    Ask a question to the Barry chatbot. Uses RAG against the knowledgebase.
    """
    try:
        # 1. Retrieve context
        context = chatbot_engine.retrieve_context(request.query)
        # 2. Generate answer
        answer = chatbot_engine.generate_response(request.query, context)
        
        return {
            "query": request.query,
            "answer": answer,
            "session_id": request.session_id or "new_session_123",
            "sources_used": True if context else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/faqs")
async def get_faqs(limit: int = 10):
    """
    Generate or retrieve FAQs based on frequently asked operations.
    """
    try:
        faqs = chatbot_engine.extract_faqs()
        return {"faqs": faqs[:limit]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
