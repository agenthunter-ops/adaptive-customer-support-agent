"""
FastAPI REST interface (JSON in/out).
Ideal for integration with mobile / web clients.
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.routing.workflow_router import get_conversation_agent
from src.core.memory import push_history

router = APIRouter(tags=["chat"])


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    agent = get_conversation_agent()
    try:
        reply = await agent(session_id=req.session_id, user_text=req.message)
        await push_history(req.session_id, {"role": "user", "content": req.message})
        await push_history(req.session_id, {"role": "assistant", "content": reply})
        return {"reply": reply}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
