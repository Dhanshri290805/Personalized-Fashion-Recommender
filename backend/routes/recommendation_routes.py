from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from backend.services.recommendation_service import get_recommendations, get_outfit, get_all_items, process_feedback

router = APIRouter()

class Preferences(BaseModel):
    category: Optional[str] = ""
    color: Optional[str] = ""
    style: Optional[str] = ""
    occasion: Optional[str] = ""
    budget: Optional[float] = None
    gender: Optional[str] = ""

class Feedback(BaseModel):
    item_id: int
    user_id: int
    feedback_type: str

@router.post("/recommend")
def recommend(prefs: Preferences):
    recs = get_recommendations(prefs.dict())
    return {"recommendations": recs}

@router.post("/outfit")
def outfit(prefs: Preferences):
    out = get_outfit(prefs.dict())
    return out

@router.get("/items")
def items():
    return {"items": get_all_items()}

@router.post("/feedback")
def feedback(fb: Feedback):
    return process_feedback(fb.item_id, fb.user_id, fb.feedback_type)
