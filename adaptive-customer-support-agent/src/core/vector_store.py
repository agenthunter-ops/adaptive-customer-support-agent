"""
Initialises a persistent FAISS or Chroma vector index and exposes a
LangChain VectorStore retriever. Abstracted so agents can import
`get_retriever()` without caring about implementation details.
"""
import logging
import os
from pathlib import Path
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain_community.vectorstores import Chroma
from .config import settings

logger = logging.getLogger(__name__)
_retriever = None


async def init_vector_store() -> None:
    global _retriever
    embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
    if settings.vector_store.lower() == "faiss":
        index_dir = Path(settings.vector_directory)
        index_dir.mkdir(parents=True, exist_ok=True)
        if not any(index_dir.iterdir()):
            # Index does not exist → create empty index
            logger.warning("FAISS index empty – initialising fresh index")
            _retriever = FAISS.from_texts(["Placeholder"], embedding=embeddings)
            _retriever.save_local(str(index_dir))
        else:
            _retriever = FAISS.load_local(str(index_dir), embeddings)
    else:
        _retriever = Chroma(
            collection_name="adaptive_support",
            embedding_function=embeddings,
            persist_directory=settings.vector_directory,
        )
    logger.info("Vector store ready (%s)", settings.vector_store)


def get_retriever():
    if _retriever is None:
        raise RuntimeError("Vector store not initialised – call init_vector_store() first")
    return _retriever.as_retriever(search_kwargs={"k": settings.similarity_top_k})
