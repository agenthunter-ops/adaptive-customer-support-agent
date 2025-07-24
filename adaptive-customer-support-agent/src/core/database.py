"""
Asynchronous MongoDB helper using Motor.
Provides a global `db` accessor lazily initialised on app startup.
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

logger = logging.getLogger(__name__)
mongo_client: AsyncIOMotorClient | None = None
db = None  # to be assigned post-initialisation


async def init_mongo() -> None:
    global mongo_client, db
    logger.info("Connecting to MongoDB...")
    mongo_client = AsyncIOMotorClient(settings.mongodb_uri, uuidRepresentation="standard")
    db = mongo_client[settings.mongodb_database]  # type: ignore[index]
    # Optionally create indexes for performance
    await db.conversations.create_index("session_id")
    logger.info("MongoDB ready!")
