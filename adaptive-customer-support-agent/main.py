"""
Application entry-point.

Bootstraps:
    • global configuration
    • background resources (Mongo, Vector store, Redis)
    • FastAPI routes
    • optional Streamlit UI (dev mode)

The file is intentionally small – core logic lives inside `src/`.
"""
import asyncio
import logging
import os
from fastapi import FastAPI
from src.core.config import settings
from src.channels.fastapi_channel import router as chat_router
from src.core.database import init_mongo
from src.core.vector_store import init_vector_store
from src.core.memory import init_memory_cache

logger = logging.getLogger(__name__)
app = FastAPI(title="Adaptive Customer Support Agent")

# --------------------------------------------------------------------------- #
# Initialise async resources on startup
# --------------------------------------------------------------------------- #
@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting application...")
    await init_mongo()
    await init_vector_store()
    await init_memory_cache()
    logger.info("Resources initialised!")


# --------------------------------------------------------------------------- #
# Register modular API routes
# --------------------------------------------------------------------------- #
app.include_router(chat_router, prefix="/api/v1")

# --------------------------------------------------------------------------- #
# Optional Streamlit UI in dev / hackathon demos
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, port=8000)  # hot-reload for DX
