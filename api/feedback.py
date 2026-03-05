from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os

router = APIRouter()

class SessionRating(BaseModel):
    session_id: str
    rating: int  # e.g., 1-5 stars
    feedback: Optional[str] = None

@router.post("/rate")
async def rate_session(rating: SessionRating):
    """
    Rate a chatbot session.
    Saves feedback locally for analysis.
    """
    if not (1 <= rating.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5 stars.")
    
    # Store feedback logic (simple JSON append for boilerplate)
    feedback_file = "chat_feedback.json"
    record = {"session_id": rating.session_id, "rating": rating.rating, "feedback": rating.feedback}
    
    try:
        records = []
        if os.path.exists(feedback_file):
            with open(feedback_file, "r") as f:
                records = json.load(f)
        records.append(record)
        with open(feedback_file, "w") as f:
            json.dump(records, f, indent=4)
            
        return {"message": "Rating submitted successfully.", "data": record}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
