"""
Lightweight rule-based escalation logic.

You can replace this with:
    • GPT classifier
    • LangChain RouterChain
    • ML model fine-tuned on escalation labels
"""
import logging
import uuid
from datetime import datetime
import re

logger = logging.getLogger(__name__)

# Example triggers – extend as needed
REGEX_PATTERNS: list[str] = [
    r"\bcomplain\b",
    r"\bfraud\b",
    r"\bscam\b",
    r"\bunauthori[sz]ed\b",
]


class EscalationAgent:
    async def requires_escalation(self, reply: str) -> bool:
        """
        Very simple heuristic:
            • look for apology + lack of confident resolution
            • regex patterns indicating serious issues
        """
        low_confidence = "I’m not sure" in reply or "I am not able" in reply
        pattern_flag = any(re.search(r, reply, re.IGNORECASE) for r in REGEX_PATTERNS)
        return low_confidence or pattern_flag

    async def create_ticket(self, session_id: str, user_message: str) -> str:
        """
        Stores ticket stub into Mongo (not shown here; replace with API call).
        Returns ticket ID string.
        """
        ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
        logger.info("Escalation ticket %s created for session %s | msg=%s",
                    ticket_id, session_id, user_message[:50])
        # TODO: persist ticket to `db.tickets.insert_one({...})`
        return ticket_id
