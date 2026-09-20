import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from ai_service import analyze_process, preflight

app = FastAPI(title="Assumption Gap API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent / "data" / "process.json"


class AnalyzeProcessRequest(BaseModel):
    process: str = Field(min_length=1)
    documents: list[str] = Field(default_factory=list)
    rejection_reasons: list[str] = Field(default_factory=list)


class PreflightRequest(BaseModel):
    process: str = Field(min_length=1)
    user_inputs: dict[str, Any] = Field(default_factory=dict)


def load_process() -> dict:
    with DATA_PATH.open(encoding="utf-8") as process_file:
        return json.load(process_file)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/api/process")
def get_process() -> dict:
    return load_process()


@app.post("/api/analyze-process")
def analyze_process_endpoint(request: AnalyzeProcessRequest) -> dict:
    return analyze_process(request.process, request.documents, request.rejection_reasons)


@app.post("/api/preflight")
def preflight_endpoint(request: PreflightRequest) -> dict:
    return preflight(request.process, request.user_inputs)
