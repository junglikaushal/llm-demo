from fastapi import APIRouter, HTTPException

from app.schemas import AskRequest, AskResponse
from app.services.llm_service import LLMProviderError, LLMTimeoutError, ask_llm

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/ask")
async def ask(request: AskRequest) -> AskResponse:
    try:
        return await ask_llm(request.question)
    except LLMTimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc)) from exc
    except LLMProviderError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
