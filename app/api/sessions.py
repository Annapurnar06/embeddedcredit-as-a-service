from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.session import LendingSession, SessionState
from app.schemas.session import SessionCreate, SessionResponse

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("/", response_model=SessionResponse, status_code=201)
async def create_session(
    payload: SessionCreate, db: AsyncSession = Depends(get_db)
) -> LendingSession:
    session = LendingSession(
        lender_id=payload.lender_id,
        channel=payload.channel,
        channel_user_id=payload.channel_user_id,
        segment=payload.segment,
        language=payload.language,
        state=SessionState.UNVERIFIED,
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: UUID, db: AsyncSession = Depends(get_db)) -> LendingSession:
    result = await db.execute(select(LendingSession).where(LendingSession.id == session_id))
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return session
