"""Chat API -- generic endpoint for all channels."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.agent.runtime import AgentRuntime
from app.gateway.channels import OutgoingMessage, get_adapter
from app.gateway.session_manager import SessionManager

router = APIRouter(prefix="/api/chat", tags=["chat"])

_session_manager = SessionManager()
_runtime = AgentRuntime()


class ChatRequest(BaseModel):
    channel: str = "web"
    channel_user_id: str
    lender_id: str = "DEFAULT_LENDER"
    content: str
    segment: str | None = None
    language: str = "hi"


class ChatResponseModel(BaseModel):
    session_id: str
    state: str
    response: str
    tools_called: list[str] = []
    channel: str = "web"


@router.post("/message", response_model=ChatResponseModel)
async def send_message(req: ChatRequest) -> ChatResponseModel:
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    session = _session_manager.get_or_create(
        channel=req.channel,
        channel_user_id=req.channel_user_id,
        lender_id=req.lender_id,
        segment=req.segment,
        language=req.language,
    )

    turn = await _runtime.process_message(session, req.content)

    return ChatResponseModel(
        session_id=str(session.session_id),
        state=session.state.value,
        response=turn.agent_response,
        tools_called=turn.tools_called,
        channel=req.channel,
    )


@router.post("/webhook/whatsapp")
async def whatsapp_webhook(payload: dict) -> dict:
    """WhatsApp BSP webhook handler."""
    adapter = get_adapter("whatsapp")
    incoming = adapter.parse_incoming(payload)

    if not incoming.content:
        return {"status": "ignored", "reason": "empty message"}

    session = _session_manager.get_or_create(
        channel="whatsapp",
        channel_user_id=incoming.channel_user_id,
        lender_id="DEFAULT_LENDER",
    )

    turn = await _runtime.process_message(session, incoming.content)

    outgoing = OutgoingMessage(
        channel="whatsapp",
        channel_user_id=incoming.channel_user_id,
        content=turn.agent_response,
    )
    response_payload = adapter.format_outgoing(outgoing)

    return {"status": "sent", "payload": response_payload}


@router.get("/sessions/active")
async def active_sessions() -> dict:
    return {"active_sessions": _session_manager.active_count}
