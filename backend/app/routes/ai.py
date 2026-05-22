from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.ai_service import extract_structured_meeting
from app.crud.meeting import save_ai_generated

router = APIRouter()


@router.post("/ai/extract", status_code=status.HTTP_201_CREATED)
def ai_extract(transcript: dict, db: Session = Depends(get_db)):
    """Accept a JSON body with 'title' and 'raw_text' and run AI/NLP extraction."""
    title = transcript.get("title")
    raw = transcript.get("raw_text")
    if not raw:
        raise HTTPException(status_code=400, detail="raw_text is required")

    try:
        structured = extract_structured_meeting(raw, title=title)
        saved = save_ai_generated(db, structured)
        return saved
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
