from fastapi import APIRouter

from app.schemas import AskRequest, AskResponse

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.post("/ask")
def ask(request: AskRequest) -> AskResponse:
    """
    Ask a question (test endpoint — not wired to LLM yet).
    """
    return AskResponse(
        answer="This is a placeholder answer.",
        confidence=0.5,
        topic="placeholder",
        token_used=0,
    )
