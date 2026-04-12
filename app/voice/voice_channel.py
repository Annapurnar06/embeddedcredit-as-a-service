"""Voice channel adapter -- handles voice call sessions via Cartesia TTS + STT."""

from __future__ import annotations

import base64
import uuid
from dataclasses import dataclass
from typing import Any

from app.agent.runtime import AgentRuntime
from app.core.audit import AuditTrail
from app.core.logging import get_logger
from app.gateway.session_manager import SessionManager
from app.voice.cartesia_client import (
    CartesiaSTTClient,
    CartesiaTTSClient,
    VoiceConfig,
    get_voice_for_segment,
)


def _encode_audio(audio_bytes: bytes) -> str:
    if audio_bytes:
        return base64.b64encode(audio_bytes).decode()
    return ""


logger = get_logger(__name__)


@dataclass
class VoiceCallState:
    call_id: str
    session_id: uuid.UUID
    channel_user_id: str
    lender_id: str
    language: str = "hi"
    segment: str | None = None
    voice_config: VoiceConfig | None = None
    turn_count: int = 0
    total_audio_ms: int = 0
    active: bool = True


class VoiceChannel:
    """Manages voice call sessions -- STT input, agent processing, TTS output."""

    def __init__(
        self,
        tts_client: CartesiaTTSClient | None = None,
        stt_client: CartesiaSTTClient | None = None,
        runtime: AgentRuntime | None = None,
        session_manager: SessionManager | None = None,
        audit: AuditTrail | None = None,
    ) -> None:
        self.tts = tts_client or CartesiaTTSClient()
        self.stt = stt_client or CartesiaSTTClient()
        self.runtime = runtime or AgentRuntime()
        self.sessions = session_manager or SessionManager()
        self.audit = audit or AuditTrail()
        self._calls: dict[str, VoiceCallState] = {}

    async def start_call(
        self,
        channel_user_id: str,
        lender_id: str,
        language: str = "hi",
        segment: str | None = None,
    ) -> dict[str, Any]:
        call_id = str(uuid.uuid4())

        agent_session = self.sessions.get_or_create(
            channel="voice",
            channel_user_id=channel_user_id,
            lender_id=lender_id,
            segment=segment,
            language=language,
        )

        voice_config = get_voice_for_segment(segment or "", language)

        call_state = VoiceCallState(
            call_id=call_id,
            session_id=agent_session.session_id,
            channel_user_id=channel_user_id,
            lender_id=lender_id,
            language=language,
            segment=segment,
            voice_config=voice_config,
        )
        self._calls[call_id] = call_state

        greeting = self._get_greeting(segment, language)
        tts_result = await self.tts.synthesize(greeting, voice_config)

        self.audit.log_event(
            session_id=agent_session.session_id,
            event_type="VOICE_CALL_STARTED",
            event_data={"call_id": call_id, "language": language, "segment": segment or ""},
            lender_id=lender_id,
        )

        logger.info(
            "voice_call_started",
            call_id=call_id,
            session_id=str(agent_session.session_id),
            language=language,
        )

        return {
            "call_id": call_id,
            "session_id": str(agent_session.session_id),
            "greeting_audio": _encode_audio(tts_result.audio_bytes),
            "greeting_text": greeting,
            "audio_format": tts_result.format,
            "duration_ms": tts_result.duration_ms,
        }

    async def process_audio_turn(
        self,
        call_id: str,
        audio_bytes: bytes,
    ) -> dict[str, Any]:
        call_state = self._calls.get(call_id)
        if not call_state or not call_state.active:
            return {"error": "Call not found or ended", "call_id": call_id}

        stt_result = await self.stt.transcribe(audio_bytes, language=call_state.language)

        if stt_result.error or not stt_result.text.strip():
            fallback = (
                "Mujhe sunaai nahi diya, kya aap dobara bol sakte hain?"
                if call_state.language == "hi"
                else "I couldn't hear that, could you repeat?"
            )
            tts_result = await self.tts.synthesize(fallback, call_state.voice_config)
            return {
                "call_id": call_id,
                "transcription": "",
                "response_text": fallback,
                "response_audio": _encode_audio(tts_result.audio_bytes),
                "audio_format": tts_result.format,
                "stt_error": stt_result.error,
            }

        borrower_text = stt_result.text

        agent_session = self.sessions.get_or_create(
            channel="voice",
            channel_user_id=call_state.channel_user_id,
            lender_id=call_state.lender_id,
            segment=call_state.segment,
            language=call_state.language,
        )

        turn = await self.runtime.process_message(agent_session, borrower_text)

        tts_result = await self.tts.synthesize(turn.agent_response, call_state.voice_config)

        call_state.turn_count += 1
        call_state.total_audio_ms += tts_result.duration_ms

        self.audit.log_event(
            session_id=call_state.session_id,
            event_type="VOICE_TURN",
            event_data={
                "call_id": call_id,
                "turn": call_state.turn_count,
                "stt_confidence": stt_result.confidence,
                "tools_called": turn.tools_called,
                "tts_duration_ms": tts_result.duration_ms,
            },
            lender_id=call_state.lender_id,
        )

        return {
            "call_id": call_id,
            "transcription": borrower_text,
            "stt_confidence": stt_result.confidence,
            "response_text": turn.agent_response,
            "response_audio": _encode_audio(tts_result.audio_bytes),
            "audio_format": tts_result.format,
            "duration_ms": tts_result.duration_ms,
            "tools_called": turn.tools_called,
            "session_state": agent_session.state.value,
            "turn_number": call_state.turn_count,
        }

    async def end_call(self, call_id: str) -> dict[str, Any]:
        call_state = self._calls.get(call_id)
        if not call_state:
            return {"error": "Call not found", "call_id": call_id}

        call_state.active = False

        self.audit.log_event(
            session_id=call_state.session_id,
            event_type="VOICE_CALL_ENDED",
            event_data={
                "call_id": call_id,
                "total_turns": call_state.turn_count,
                "total_audio_ms": call_state.total_audio_ms,
            },
            lender_id=call_state.lender_id,
        )

        summary = {
            "call_id": call_id,
            "session_id": str(call_state.session_id),
            "total_turns": call_state.turn_count,
            "total_audio_ms": call_state.total_audio_ms,
            "language": call_state.language,
            "segment": call_state.segment,
        }

        del self._calls[call_id]
        return summary

    def get_active_calls(self) -> list[dict[str, Any]]:
        return [
            {
                "call_id": cs.call_id,
                "session_id": str(cs.session_id),
                "turns": cs.turn_count,
                "language": cs.language,
            }
            for cs in self._calls.values()
            if cs.active
        ]

    def _get_greeting(self, segment: str | None, language: str) -> str:
        if language == "hi":
            return (
                "Namaste! Main aapka lending assistant hoon. "
                "Main aapki loan ki zaroorat mein madad kar sakta hoon. "
                "Kya aap apni jaankari dena chahenge?"
            )
        return (
            "Hello! I am your lending assistant. "
            "I can help you with your loan needs. "
            "Would you like to share your details?"
        )

    async def close(self) -> None:
        await self.tts.close()
        await self.stt.close()
