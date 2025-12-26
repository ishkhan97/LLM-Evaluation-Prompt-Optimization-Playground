# api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import asyncio

from db import init_db, insert_run
from llm_client import get_llm, LLMResponse


app = FastAPI(
    title="LLM Evaluation Playground",
    description="Run and log LLM experiments with latency, cost, and quality metrics.",
    version="0.1.0",
)


# ---------- Startup ----------

@app.on_event("startup")
async def startup_event():
    """
    Initialize database and other resources.
    """
    init_db()


# ---------- Request / Response Models ----------

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    model: str = Field(default="mock")


class GenerateResponse(BaseModel):
    output: str
    latency_ms: float
    tokens: int
    cost: float


# ---------- API Endpoints ----------

@app.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """
    Run an LLM generation and log the result.
    """
    try:
        llm = get_llm(request.model)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Run inference in a thread to avoid blocking the event loop
    response: LLMResponse = await asyncio.to_thread(
        llm.generate,
        request.prompt
    )

    # Log to database (also offloaded)
    await asyncio.to_thread(
        insert_run,
        request.prompt,
        request.model,
        response.text,
        response.latency_ms,
        response.tokens,
        response.cost,
    )

    return GenerateResponse(
        output=response.text,
        latency_ms=response.latency_ms,
        tokens=response.tokens,
        cost=response.cost,
    )
