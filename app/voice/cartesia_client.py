"""Cartesia Voice AI client -- text-to-speech and speech-to-text for borrower voice interactions."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

CARTESIA_TTS_URL = "https://api.cartesia.ai/tts/bytes"
CARTESIA_WS_URL = "wss://api.cartesia.ai/tts/websocket"

VOICE_MAP: dict[str, str] = {
    "hi_male": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "hi_female": "2ee87190-8f84-4925-97da-e52547f9462c",
    "en_male": "79a125e8-cd45-4c13-8a67-188112f4dd22",
    "en_female": "b7d50908-b17c-442d-ad8d-810c63997ed9",
    "gu_male": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "bn_male": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "ta_male": "a0e99841-438c-4a64-b679-ae501e7d6091",
    "mr_male": "a0e99841-438c-4a64-b679-ae501e7d6091",
}

LANGUAGE_MODEL_MAP: dict[str, str] = {
    "hi": "sonic-2-2025-04-16",
    "en": "sonic-2-2025-04-16",
    "gu": "sonic-2-2025-04-16",
    "bn": "sonic-2-2025-04-16",
    "ta": "sonic-2-2025-04-16",
    "mr": "sonic-2-2025-04-16",
}


@dataclass
class VoiceConfig:
    voice_id: str = ""
    language: str = "hi"
    speed: float = 1.0
    emotion: str = "neutral"
    output_format: str = "pcm_16000"

    def resolve_voice_id(self, gender: str = "male") -> str:
        if self.voice_id:
            return self.voice_id
        key = f"{self.language}_{gender}"
        return VOICE_MAP.get(key, VOICE_MAP["hi_male"])


@dataclass
class TTSResult:
    audio_bytes: bytes
    duration_ms: int = 0
    format: str = "pcm_16000"
    voice_id: str = ""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    error: str | None = None


@dataclass
class STTResult:
    text: str = ""
    language_detected: str = ""
    confidence: float = 0.0
    segments: list[dict[str, Any]] = field(default_factory=list)
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    error: str | None = None


class CartesiaTTSClient:
    """Cartesia text-to-speech client for generating voice responses."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.cartesia_api_key
        self._http = httpx.AsyncClient(timeout=30.0)

    async def synthesize(
        self,
        text: str,
        voice_config: VoiceConfig | None = None,
        gender: str = "male",
    ) -> TTSResult:
        config = voice_config or VoiceConfig()
        voice_id = config.resolve_voice_id(gender)
        model_id = LANGUAGE_MODEL_MAP.get(config.language, "sonic-2-2025-04-16")

        if not self.api_key:
            return self._mock_synthesize(text, voice_id)

        payload = {
            "model_id": model_id,
            "transcript": text,
            "voice": {
                "mode": "id",
                "id": voice_id,
            },
            "output_format": {
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 16000,
            },
            "language": config.language,
        }

        try:
            resp = await self._http.post(
                CARTESIA_TTS_URL,
                json=payload,
                headers={
                    "X-API-Key": self.api_key,
                    "Cartesia-Version": "2024-06-10",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            audio_data = resp.content
            duration_ms = int(len(audio_data) / (16000 * 2) * 1000)

            logger.info(
                "cartesia_tts_success",
                text_length=len(text),
                audio_bytes=len(audio_data),
                duration_ms=duration_ms,
                voice_id=voice_id,
            )

            return TTSResult(
                audio_bytes=audio_data,
                duration_ms=duration_ms,
                format=config.output_format,
                voice_id=voice_id,
            )
        except httpx.HTTPStatusError as e:
            logger.error("cartesia_tts_error", status=e.response.status_code, detail=str(e))
            return TTSResult(audio_bytes=b"", error=f"Cartesia TTS error: {e.response.status_code}")
        except Exception as e:
            logger.error("cartesia_tts_exception", error=str(e))
            return TTSResult(audio_bytes=b"", error=str(e))

    def _mock_synthesize(self, text: str, voice_id: str) -> TTSResult:
        fake_samples = len(text) * 160
        audio = b"\x00\x00" * fake_samples
        return TTSResult(
            audio_bytes=audio,
            duration_ms=int(fake_samples / 16),
            format="pcm_16000",
            voice_id=voice_id,
        )

    async def close(self) -> None:
        await self._http.aclose()


class CartesiaSTTClient:
    """Speech-to-text client -- wraps Deepgram/Whisper for input transcription.

    Cartesia is TTS-focused; STT uses a complementary provider.
    This abstraction allows swapping providers without changing the voice channel.
    """

    def __init__(self, api_key: str | None = None, provider: str = "deepgram") -> None:
        self.api_key = api_key or settings.stt_api_key
        self.provider = provider
        self._http = httpx.AsyncClient(timeout=30.0)

    async def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "hi",
        sample_rate: int = 16000,
    ) -> STTResult:
        if not self.api_key:
            return self._mock_transcribe(audio_bytes, language)

        if self.provider == "deepgram":
            return await self._transcribe_deepgram(audio_bytes, language, sample_rate)

        return STTResult(error=f"Unsupported STT provider: {self.provider}")

    async def _transcribe_deepgram(
        self,
        audio_bytes: bytes,
        language: str,
        sample_rate: int,
    ) -> STTResult:
        lang_map = {"hi": "hi", "en": "en-IN", "gu": "gu", "bn": "bn", "ta": "ta", "mr": "mr"}
        dg_lang = lang_map.get(language, "hi")

        try:
            resp = await self._http.post(
                "https://api.deepgram.com/v1/listen",
                content=audio_bytes,
                headers={
                    "Authorization": f"Token {self.api_key}",
                    "Content-Type": f"audio/l16;rate={sample_rate}",
                },
                params={
                    "model": "nova-2",
                    "language": dg_lang,
                    "smart_format": "true",
                    "punctuate": "true",
                },
            )
            resp.raise_for_status()
            data = resp.json()
            alt = data.get("results", {}).get("channels", [{}])[0].get("alternatives", [{}])[0]
            return STTResult(
                text=alt.get("transcript", ""),
                language_detected=language,
                confidence=alt.get("confidence", 0.0),
            )
        except Exception as e:
            logger.error("deepgram_stt_error", error=str(e))
            return STTResult(error=str(e))

    def _mock_transcribe(self, audio_bytes: bytes, language: str) -> STTResult:
        return STTResult(
            text="Namaste, mujhe loan chahiye" if language == "hi" else "Hello, I need a loan",
            language_detected=language,
            confidence=0.92,
        )

    async def close(self) -> None:
        await self._http.aclose()


def get_voice_for_segment(segment_id: str, language: str = "hi") -> VoiceConfig:
    empathetic_segments = {
        "DOMESTIC_WORKER",
        "CONSTRUCTION_WORKER",
        "STREET_VENDOR",
        "SHG_MEMBER",
        "FISHERY",
    }
    professional_segments = {
        "FPO_ENTITY",
        "NBFC_BC",
        "MSE_MANUFACTURING",
        "TRADER_AGRI",
    }

    emotion = "neutral"
    if segment_id in empathetic_segments:
        emotion = "warm"
    elif segment_id in professional_segments:
        emotion = "professional"

    return VoiceConfig(
        language=language,
        emotion=emotion,
        speed=0.9 if segment_id in empathetic_segments else 1.0,
    )
