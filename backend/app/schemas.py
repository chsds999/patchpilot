from typing import List, Literal, Optional
from pydantic import BaseModel, Field

Strictness = Literal["gentle", "balanced", "strict"]

class ReviewRequest(BaseModel):
    language: str = Field(..., examples=["python", "typescript", "java", "c++"])
    code: str = Field(..., min_length=1)
    goals: List[str] = Field(default_factory=lambda: ["readability", "correctness"])
    context: Optional[str] = Field(
        default=None,
        description="Extra context like constraints, intended behavior, or environment"
    )
    strictness: Strictness = "balanced"

class ReviewResponse(BaseModel):
    review_markdown: str
    meta: dict
