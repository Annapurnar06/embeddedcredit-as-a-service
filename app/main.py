from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.audit import router as audit_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.lender import router as lender_router
from app.api.loans import router as loans_router
from app.api.memory import router as memory_router
from app.api.sessions import router as sessions_router
from app.api.voice import router as voice_router
from app.core.logging import setup_logging
from app.core.redis import close_redis
from app.segments.loader import SegmentRegistry


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    setup_logging()
    SegmentRegistry.load_from_directory("segments")
    yield
    await close_redis()


app = FastAPI(
    title="LendingOS-India",
    description="AI-native lending operating system for Indian financial inclusion — "
    "voice AI (Cartesia), persistent memory (mem0), 38 borrower segments, 60 lending tools",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(sessions_router)
app.include_router(loans_router)
app.include_router(audit_router)
app.include_router(chat_router)
app.include_router(voice_router)
app.include_router(memory_router)
app.include_router(lender_router)
