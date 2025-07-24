"""
Ephemeral memory cache using Redis Streams (optional).
Allows agents to store / retrieve recent conversation steps quickly
without Mongo round-trip. Falls back to in-process dict if Redis absent.
"""
import json
import logging
from redis.asyncio import from_url
from .config import settings

logger = logging.getLogger(__name__)
_redis = None
_fallback: dict[str, list[dict]] = {}     # for local dev


async def init_memory_cache() -> None:
    global _redis
    try:
        _redis = from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
        await _redis.ping()
        logger.info("Redis memory cache ready!")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Redis unavailable → using in-process fallback (%s)", exc)


async def push_history(session_id: str, message: dict) -> None:
    if _redis:
        await _redis.xadd(session_id, message)
    else:
        _fallback.setdefault(session_id, []).append(message)


async def get_history(session_id: str, limit: int = 15) -> list[dict]:
    if _redis:
        stream = await _redis.xrevrange(session_id, count=limit)
        return [json.loads(m[1]["data"]) for m in reversed(stream)]
    return _fallback.get(session_id, [])[-limit:]
