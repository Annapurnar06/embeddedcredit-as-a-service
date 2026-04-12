"""Voice API -- endpoints for Cartesia-powered voice lending conversations."""

from __future__ import annotations

import base64

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.logging import get_logger
from app.voice.voice_channel import VoiceChannel

router = APIRouter(prefix="/api/voice", tags=["voice"])
logger = get_logger(__name__)

_voice_channel = VoiceChannel()


class StartCallRequest(BaseModel):
    channel_user_id: str
    lender_id: str = "DEFAULT_LENDER"
    language: str = "hi"
    segment: str | None = None


class StartCallResponse(BaseModel):
    call_id: str
    session_id: str
    greeting_text: str
    greeting_audio_base64: str = ""
    audio_format: str = "pcm_16000"
    duration_ms: int = 0


class AudioTurnRequest(BaseModel):
    call_id: str
    audio_base64: str


class AudioTurnResponse(BaseModel):
    call_id: str
    transcription: str = ""
    stt_confidence: float = 0.0
    response_text: str = ""
    response_audio_base64: str = ""
    audio_format: str = "pcm_16000"
    duration_ms: int = 0
    tools_called: list[str] = []
    session_state: str = ""
    turn_number: int = 0
    error: str | None = None


class EndCallResponse(BaseModel):
    call_id: str
    session_id: str = ""
    total_turns: int = 0
    total_audio_ms: int = 0
    language: str = ""
    segment: str | None = None


@router.post("/start", response_model=StartCallResponse)
async def start_voice_call(req: StartCallRequest) -> StartCallResponse:
    if not req.channel_user_id.strip():
        raise HTTPException(status_code=400, detail="channel_user_id required")

    result = await _voice_channel.start_call(
        channel_user_id=req.channel_user_id,
        lender_id=req.lender_id,
        language=req.language,
        segment=req.segment,
    )
    return StartCallResponse(
        call_id=result["call_id"],
        session_id=result["session_id"],
        greeting_text=result["greeting_text"],
        greeting_audio_base64=result.get("greeting_audio", ""),
        audio_format=result.get("audio_format", "pcm_16000"),
        duration_ms=result.get("duration_ms", 0),
    )


@router.post("/turn", response_model=AudioTurnResponse)
async def process_voice_turn(req: AudioTurnRequest) -> AudioTurnResponse:
    if not req.call_id.strip():
        raise HTTPException(status_code=400, detail="call_id required")

    try:
        audio_bytes = base64.b64decode(req.audio_base64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 audio") from exc

    result = await _voice_channel.process_audio_turn(
        call_id=req.call_id,
        audio_bytes=audio_bytes,
    )

    if "error" in result and result["error"]:
        return AudioTurnResponse(call_id=req.call_id, error=result["error"])

    return AudioTurnResponse(
        call_id=result["call_id"],
        transcription=result.get("transcription", ""),
        stt_confidence=result.get("stt_confidence", 0.0),
        response_text=result.get("response_text", ""),
        response_audio_base64=result.get("response_audio", ""),
        audio_format=result.get("audio_format", "pcm_16000"),
        duration_ms=result.get("duration_ms", 0),
        tools_called=result.get("tools_called", []),
        session_state=result.get("session_state", ""),
        turn_number=result.get("turn_number", 0),
    )


@router.post("/end/{call_id}", response_model=EndCallResponse)
async def end_voice_call(call_id: str) -> EndCallResponse:
    result = await _voice_channel.end_call(call_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return EndCallResponse(**result)


@router.get("/calls/active")
async def active_calls() -> dict:
    calls = _voice_channel.get_active_calls()
    return {"active_calls": calls, "count": len(calls)}
