"""
LLM-backed conversational agent.
Maintains context, queries RAG agent when needed,
and triggers escalation if confidence low.
Built with LangGraph for stateful workflows.
"""
import logging
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from src.core.llm_client import chat
from src.core.config import settings
from .rag_agent import RagAgent
from .escalation_agent import EscalationAgent
from .intent_classifier import get_intent_classifier

logger = logging.getLogger(__name__)


class ConvState(TypedDict):
    messages: Annotated[list, add_messages]            # conversation history
    session_id: str
    requires_escalation: bool | None


class ConversationAgent:
    """
    Composable LangGraph that:
        1. Classifies user intent
        2. Retrieves contextual docs via RagAgent
        3. Generates response
        4. Decides whether to escalate
    """

    def __init__(self) -> None:
        self.rag = RagAgent()
        self.escalator = EscalationAgent()
        self.graph = self._build_graph()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    async def __call__(self, session_id: str, user_text: str) -> str:
        """
        Entry point for FastAPI / Streamlit channel.
        Returns the AI's reply (string). All state is persisted via memory.
        """
        state = {
            "messages": [HumanMessage(content=user_text)],
            "session_id": session_id,
            "requires_escalation": None,
        }
        result = await self.graph.invoke(state)
        reply: AIMessage = result["messages"][-1]
        return reply.content

    # ------------------------------------------------------------------ #
    # Internal LangGraph definition
    # ------------------------------------------------------------------ #
    def _build_graph(self):
        graph_builder = StateGraph(ConvState)

        # Node 1 – Intent classification
        async def node_intent(state: ConvState):
            user_msg: HumanMessage = state["messages"][-1]
            intent, confidence = get_intent_classifier().classify(user_msg.content)
            # Append system comment for transparency (not returned to user)
            system_hint = SystemMessage(
                content=f"[debug] intent={intent} prob={confidence:.2f}"
            )
            return {"messages": [system_hint]}

        graph_builder.add_node("intent", node_intent)

        # Node 2 – RAG retrieve + draft answer
        async def node_draft(state: ConvState):
            user_msg: HumanMessage = state["messages"][-1]
            context_docs = await self.rag.retrieve(user_msg.content)
            logger.debug("RAG returned %d docs", len(context_docs))

            # Build prompt with retrieved context
            messages = [
                SystemMessage(content=(
                    "You are an expert banking customer support agent. "
                    "Answer user queries politely, concisely, and accurately."
                )),
                *context_docs,             # inject as system messages
                *state["messages"],        # conversation so far
            ]
            draft_reply = await chat([m.to_dict() for m in messages])
            return {"messages": [AIMessage(content=draft_reply)]}

        graph_builder.add_node("draft", node_draft)

        # Node 3 – Check if escalation needed
        async def node_escalate(state: ConvState):
            last_ai: AIMessage = state["messages"][-1]
            requires = await self.escalator.requires_escalation(last_ai.content)
            return {"requires_escalation": requires}

        graph_builder.add_node("check", node_escalate)

        # Conditional branch – escalate or end
        def decide(state: ConvState):                  # sync fn allowed
            return "escalate" if state["requires_escalation"] else END

        graph_builder.add_conditional_edge("check", decide, {"escalate": "escalate"})

        # Node 4 – Escalation
        async def node_escalate_flow(state: ConvState):
            user_msg: HumanMessage = state["messages"][-2]   # last human
            ticket_id = await self.escalator.create_ticket(
                session_id=state["session_id"], user_message=user_msg.content
            )
            reply = (
                "I'm transferring you to a human specialist. "
                f"Your ticket reference is **{ticket_id}**. "
                "Please hold while I connect you."
            )
            return {"messages": [AIMessage(content=reply)]}

        graph_builder.add_node("escalate", node_escalate_flow)

        # Wire edges
        graph_builder.add_edge(START, "intent")
        graph_builder.add_edge("intent", "draft")
        graph_builder.add_edge("draft", "check")
        graph_builder.set_entry_point(START)

        return graph_builder.compile()
