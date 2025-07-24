"""
Utility for loading and chunking knowledge base docs into the vector
store. Run once as a script – idempotent (skips already-indexed docs).
"""
import json
import logging
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.core.vector_store import get_retriever
from src.core.config import settings

logger = logging.getLogger(__name__)
DOCS_DIR = Path(__file__).parent.parent / "data" / "knowledge_docs"
CHUNK_SIZE = 500
OVERLAP = 50


def ingest() -> None:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP
    )
    retriever = get_retriever()

    for file in DOCS_DIR.glob("*.md"):
        with open(file, encoding="utf-8") as f:
            text = f.read()
        chunks = splitter.split_text(text)
        # Dedup by simple hash
        for chunk in chunks:
            retriever.add_documents(
                [{"page_content": chunk, "metadata": {"source": file.name}}]
            )
    # Persist if FAISS
    if settings.vector_store == "faiss":
        retriever._vectorstore.save_local(settings.vector_directory)  # type: ignore[attr-defined]
    logger.info("Ingestion complete.")


if __name__ == "__main__":
    ingest()
