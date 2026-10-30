"""FastAPI entrypoint. Runs behind Lambda Web Adapter on :8080.

CloudFront forwards the full path, so every route lives under /api.
"""

import os

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import mbti_engine
from .questions import QUESTIONS, Dichotomy

# Swagger UI pulls scripts from a CDN, which the CloudFront CSP blocks, so Terraform turns
# the docs off in AWS (ENABLE_API_DOCS=false). They stay on for local development.
_docs_enabled = os.environ.get("ENABLE_API_DOCS", "true").strip().lower() != "false"

app = FastAPI(
    title="MBTI Assessment API",
    version="1.0.0",
    docs_url="/api/docs" if _docs_enabled else None,
    redoc_url=None,
    openapi_url="/api/openapi.json" if _docs_enabled else None,
)

# In production the browser and API share the CloudFront origin, so no CORS is needed;
# Terraform sets this to "" there. The fallback covers local frontend dev servers.
_cors_origins = [
    o.strip()
    for o in os.environ.get("CORS_ALLOW_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
    if o.strip()
]
if _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        # x-amz-content-sha256 is required on POST bodies sent through CloudFront OAC.
        allow_headers=["Content-Type", "x-amz-content-sha256"],
        allow_credentials=False,
        max_age=600,
    )


class QuestionOut(BaseModel):
    id: str
    text: str
    text_en: str
    dichotomy: Dichotomy
    direction: int


class Answer(BaseModel):
    question_id: str = Field(max_length=16)
    score: int = Field(ge=-mbti_engine.MAX_SCORE, le=mbti_engine.MAX_SCORE)


class SubmitRequest(BaseModel):
    answers: list[Answer] = Field(min_length=len(mbti_engine.DICHOTOMIES), max_length=len(QUESTIONS))


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "service": "mbti-backend"}


@app.get("/api/questions", response_model=list[QuestionOut])
def get_questions(count: int = Query(25, description="One of 25, 50, 75, 100")) -> list[QuestionOut]:
    if count not in mbti_engine.ALLOWED_COUNTS:
        raise HTTPException(422, f"count must be one of {list(mbti_engine.ALLOWED_COUNTS)}")
    return [
        QuestionOut(id=q.id, text=q.text, text_en=q.text_en, dichotomy=q.dichotomy, direction=q.direction)
        for q in mbti_engine.sample_questions(count)
    ]


@app.post("/api/submit")
def submit(body: SubmitRequest) -> dict:
    try:
        scores = mbti_engine.score_answers((a.question_id, a.score) for a in body.answers)
    except mbti_engine.ScoringError as exc:
        raise HTTPException(422, str(exc)) from exc
    return mbti_engine.build_result(scores)
