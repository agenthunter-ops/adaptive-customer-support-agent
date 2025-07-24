"""
Separate router exposing `/intent` endpoint if you want to query the
classifier directly (useful for testing or analytics dashboards).
"""
from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.intent_classifier import get_intent_classifier

router = APIRouter(tags=["intent"])


class Query(BaseModel):
    text: str


@router.post("/classify")
async def classify_intent(payload: Query):
    intent, confidence = get_intent_classifier().classify(payload.text)
    return {"intent": intent, "confidence": confidence}
