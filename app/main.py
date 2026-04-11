from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.audit import router as audit_router
from app.api.chat import router as chat_router
from app.api.health import router as health_router
from app.api.loans import router as loans_router
from app.api.sessions import router as sessions_router
from app.core.logging import setup_logging
from app.core.redis import close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
    setup_logging()
    yield
    await close_redis()


app = FastAPI(
    title="LendingOS-India",
    description="AI-first lending platform for Indian financial inclusion",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(sessions_router)
app.include_router(loans_router)
app.include_router(audit_router)
app.include_router(chat_router)
