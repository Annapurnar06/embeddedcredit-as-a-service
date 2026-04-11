from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SessionCreate(BaseModel):
    lender_id: str
    channel: str
    channel_user_id: str
    segment: str | None = None
    language: str = "hi"


class SessionResponse(BaseModel):
    id: UUID
    state: str
    borrower_id: UUID | None = None
    loan_application_id: UUID | None = None
    lender_id: str
    channel: str
    segment: str | None = None
    language: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChatMessage(BaseModel):
    session_id: UUID
    content: str
    channel: str = "web"
    channel_user_id: str = ""


class ChatResponse(BaseModel):
    session_id: UUID
    response: str
    state: str
    tools_called: list[str] = []
