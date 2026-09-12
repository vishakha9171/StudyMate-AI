from pydantic import BaseModel
from typing import List, Optional


class Chunk(BaseModel):
    id: str
    text: str
    source: str
    page: int
    section: Optional[str] = None
    source_type: str


class SearchResult(BaseModel):
    id: str
    text: str
    source: str
    page: int
    section: Optional[str] = None
    score: float


class ChatRequest(BaseModel):
    question: str
    history: List[dict] = []


class ChatResponse(BaseModel):
    answer: str
    sources: List[SearchResult]
    refused: bool