"""
Unit tests for core agents (fast async style).
"""
import pytest
from src.agents.intent_classifier import get_intent_classifier
from src.agents.escalation_agent import EscalationAgent

@pytest.mark.asyncio
async def test_intent_classifier_basic():
    clf = get_intent_classifier()
    intent, prob = clf.classify("Please block my card")
    assert intent == "card_block"
    assert prob > 0.5

@pytest.mark.asyncio
async def test_escalation_logic():
    esc = EscalationAgent()
    assert await esc.requires_escalation("I am not sure how to help.") is True
    assert await esc.requires_escalation("All good!") is False
