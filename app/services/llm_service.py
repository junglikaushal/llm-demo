import json

from openai import AsynOpenAI

from app.core.config import settings
from app.schemas import AskResponse

client = AsynOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """You are a helpful assistant. Answer the user's question and \
respond ONLY with a JSON object in this exact shape, with no extra text:

{
  "answer": "<your answer to the question>",
  "confidence": <float between 0 and 1, how confident you are>,
  "topic": "<one or two word topic of the question>"
}
"""


async def ask_llm(question: str) -> AskResponse:
    response = await client.chat.completions.create(
        model=settings.openai_model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        response_format={"type": "json_schema"},
        timeout=settings.request_timeout,
    )

    raw_content = response.choices[0].message.content
    parsed = json.loads(raw_content)

    return AskResponse(
        answer=parsed["answer"],
        confidence=parsed["confidence"],
        topic=parsed["topic"],
        token_used=response.usage.total_tokens,
    )
