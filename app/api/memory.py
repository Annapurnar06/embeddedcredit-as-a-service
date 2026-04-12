"""Memory API -- endpoints for borrower memory management via mem0."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.memory.mem0_client import BorrowerMemory, Mem0Client

router = APIRouter(prefix="/api/memory", tags=["memory"])

_mem0 = Mem0Client()
_borrower_memory = BorrowerMemory(_mem0)


class AddMemoryRequest(BaseModel):
    borrower_id: str
    content: str
    metadata: dict | None = None


class SearchMemoryRequest(BaseModel):
    borrower_id: str
    query: str
    limit: int = 10


class MemoryResponse(BaseModel):
    id: str
    user_id: str
    content: str
    metadata: dict = {}
    score: float = 1.0


class ContextResponse(BaseModel):
    borrower_id: str
    context: str
    memory_count: int = 0


@router.post("/add", response_model=MemoryResponse)
async def add_memory(req: AddMemoryRequest) -> MemoryResponse:
    if not req.borrower_id.strip() or not req.content.strip():
        raise HTTPException(status_code=400, detail="borrower_id and content required")
    entry = await _mem0.add(req.borrower_id, req.content, req.metadata)
    return MemoryResponse(
        id=entry.id,
        user_id=entry.user_id,
        content=entry.content,
        metadata=entry.metadata,
        score=entry.score,
    )


@router.post("/search", response_model=list[MemoryResponse])
async def search_memory(req: SearchMemoryRequest) -> list[MemoryResponse]:
    result = await _mem0.search(req.borrower_id, req.query, req.limit)
    return [
        MemoryResponse(
            id=m.id,
            user_id=m.user_id,
            content=m.content,
            metadata=m.metadata,
            score=m.score,
        )
        for m in result.memories
    ]


@router.get("/borrower/{borrower_id}", response_model=list[MemoryResponse])
async def get_borrower_memories(borrower_id: str) -> list[MemoryResponse]:
    entries = await _mem0.get_all(borrower_id)
    return [
        MemoryResponse(
            id=e.id,
            user_id=e.user_id,
            content=e.content,
            metadata=e.metadata,
            score=e.score,
        )
        for e in entries
    ]


@router.get("/borrower/{borrower_id}/context", response_model=ContextResponse)
async def get_borrower_context(borrower_id: str, query: str = "") -> ContextResponse:
    context = await _borrower_memory.get_borrower_context(borrower_id, query)
    entries = await _mem0.get_all(borrower_id)
    return ContextResponse(
        borrower_id=borrower_id,
        context=context,
        memory_count=len(entries),
    )


@router.delete("/borrower/{borrower_id}")
async def delete_borrower_memories(borrower_id: str) -> dict:
    success = await _mem0.delete_all(borrower_id)
    return {"deleted": success, "borrower_id": borrower_id}
