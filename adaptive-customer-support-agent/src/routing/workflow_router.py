"""
Central router that receives inbound payloads and calls
ConversationAgent. Keeps FastAPI layer thin & framework-agnostic.
"""
from functools import lru_cache
from src.agents.conversation_agent import ConversationAgent

@lru_cache
def get_conversation_agent() -> ConversationAgent:
    return ConversationAgent()
