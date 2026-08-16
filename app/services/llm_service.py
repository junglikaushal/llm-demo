import json

from openai import APIError, APITimeoutError, AsyncOpenAI

from app.core.config import settings
from app.schemas import AskResponse

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are a helpful assistant. Answer the user's question and \
respond ONLY with a JSON object in this exact shape, with no extra text:

{
  "answer": "<your answer to the question>",
  "confidence": <float between 0 and 1, how confident you are>,
  "topic": "<one or two word topic of the question>"
}
"""


class LLMTimeoutError(Exception):
    """Raised when the LLM provider takes too long to respond."""


class LLMProviderError(Exception):
    """Raised when the LLM provider fails or returns something we can't use."""


async def ask_llm(question: str) -> AskResponse:
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            response_format={"type": "json_object"},
            timeout=settings.request_timeout,
        )

    except APITimeoutError as exc:
        raise LLMTimeoutError("The LLM provider took too long to respond") from exc
    except APIError as exc:
        raise LLMProviderError(f"LLM provider error: {exc}") from exc

    raw_content = response.choices[0].message.content

    try:
        parsed = json.loads(raw_content)
        result = AskResponse(
            answer=parsed["answer"],
            confidence=parsed["confidence"],
            topic=parsed["topic"],
            token_used=response.usage.total_tokens,
        )

    except (json.JSONDecodeError, KeyError, ValueError) as exc:
        raise LLMProviderError(
            f"LLM returned a response we couldn't parse: {exc}"
        ) from exc

    return result
