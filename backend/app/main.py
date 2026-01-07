import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import ReviewRequest, ReviewResponse
from .review_engine import run_review

app = FastAPI(
    title="PatchPilot API",
    version="1.0.0",
    description="AI-powered code review service"
)

allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/health")
def health_check():
    return {"ok": True}

@app.post("/api/review", response_model=ReviewResponse)
def review_code(request: ReviewRequest):
    try:
        review_md, meta = run_review(
            language=request.language,
            code=request.code,
            goals=request.goals,
            context=request.context,
            strictness=request.strictness
        )
        return ReviewResponse(review_markdown=review_md, meta=meta)

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
