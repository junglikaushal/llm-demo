from pydantic import BaseModel, ConfigDict, Field


class AskResponse(BaseModel):
    answer: str = Field(..., description="The LLM's answer to the question")
    confidence: float = Field(
        ..., ge=0, le=1, description="Confidence score between 0 and 1"
    )
    topic: str = Field(..., description="The main topic of the question")
    token_used: int = Field(..., description="Number of tokens used in the response")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "answer": "Python is a high-level programming language.",
                "confidence": 0.95,
                "topic": "Programming",
                "token_used": 42,
            }
        }
    )
