"""
Retrieval-Augmented-Generation helper.
• Performs similarity search via VectorStore
• Returns LangChain SystemMessage objects for injection
"""
import logging
from langchain.schema import SystemMessage
from src.core.vector_store import get_retriever

logger = logging.getLogger(__name__)


class RagAgent:
    async def retrieve(self, query: str) -> list[SystemMessage]:
        retriever = get_retriever()
        docs = retriever.get_relevant_documents(query)
        logger.debug("RAG retrieved %d docs for '%s'", len(docs), query[:30])
        return [
            SystemMessage(
                content=f"Context:\n{doc.page_content.strip()}",
                metadata={"source": doc.metadata.get("source", "")},
            )
            for doc in docs
        ]
