from pydantic import BaseModel, Field

from .common import Citation


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    limit: int = Field(default=5, ge=1, le=20)


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    grounded: bool = True
