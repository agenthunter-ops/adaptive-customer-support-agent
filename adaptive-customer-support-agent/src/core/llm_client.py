"""
Tiny wrapper around OpenAI ChatCompletion with sensible defaults
and retry logic. If needed, swap in Azure or Anthropic models here
without touching agent code.
"""
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential
from langchain.chat_models import ChatOpenAI
from .config import settings

logger = logging.getLogger(__name__)

# Single, shared instance for efficiency (connection pooling, etc.)
_llm = ChatOpenAI(
    model_name="gpt-4o-mini",      # switch to `gpt-4o` / enterprise tier if available
    temperature=0.2,
    openai_api_key=settings.openai_api_key,
    openai_api_base=settings.openai_api_base,
    streaming=True,
    request_timeout=30,
)


@retry(stop=stop_after_attempt(3), wait=wait_random_exponential(multiplier=1, max=10))
async def chat(messages: list[dict]) -> str:
    """
    Thin async wrapper to the underlying LangChain call.
    Accepts list of OpenAI-formatted messages.
    Retries failures with exponential back-off.
    """
    logger.debug("Invoking LLM with %d messages", len(messages))
    response = await _llm.agenerate([messages])   # returns ChatResult
    return response.generations[0][0].text.strip()
