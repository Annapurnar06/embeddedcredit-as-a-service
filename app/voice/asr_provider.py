"""Multi-provider ASR (Speech-to-Text) with automatic fallback chain.

Solves: Cartesia provides TTS only. This module provides robust STT via
Deepgram (primary) -> Google Speech (fallback) -> Bhashini (government, free).
Falls through the chain on failure so the voice agent is never fully down.
"""

from __future__ import annotations

import base64
import enum
from dataclasses import dataclass, field

import httpx

from app.core.logging import get_logger

logger = get_logger(__name__)


class ASRProvider(str, enum.Enum):
    DEEPGRAM = "deepgram"
    GOOGLE = "google"
    BHASHINI = "bhashini"


LANGUAGE_CODES: dict[str, dict[str, str]] = {
    "deepgram": {
        "hi": "hi", "en": "en-IN", "gu": "gu", "bn": "bn",
        "ta": "ta", "te": "te", "mr": "mr", "kn": "kn",
        "ml": "ml", "pa": "pa",
    },
    "google": {
        "hi": "hi-IN", "en": "en-IN", "gu": "gu-IN", "bn": "bn-IN",
        "ta": "ta-IN", "te": "te-IN", "mr": "mr-IN", "kn": "kn-IN",
        "ml": "ml-IN", "pa": "pa-IN",
    },
    "bhashini": {
        "hi": "hi", "en": "en", "gu": "gu", "bn": "bn",
        "ta": "ta", "te": "te", "mr": "mr", "kn": "kn",
        "ml": "ml", "pa": "pa",
    },
}

MOCK_TEXTS: dict[str, str] = {
    "hi": "Namaste, mujhe loan chahiye",
    "gu": "Namaste, mane loan joiye chhe",
    "ta": "Vanakkam, enakku loan venum",
    "te": "Namaskaram, naaku loan kavali",
    "bn": "Nomoshkar, amar loan dorkar",
    "mr": "Namaskar, mala loan pahije",
    "kn": "Namaskara, nanage loan beku",
    "ml": "Namaskaram, enikku loan venam",
    "pa": "Sat sri akaal, mainu loan chahida hai",
    "en": "Hello, I need a loan",
}


@dataclass
class ASRResult:
    text: str = ""
    language_detected: str = ""
    confidence: float = 0.0
    provider_used: str = ""
    alternatives: list[str] = field(default_factory=list)
    duration_ms: int = 0
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.error is None and bool(self.text.strip())


@dataclass
class ASRConfig:
    deepgram_api_key: str = ""
    google_api_key: str = ""
    bhashini_api_key: str = ""
    bhashini_user_id: str = ""
    bhashini_pipeline_id: str = "64392f96daac500b55c543cd"
    fallback_order: list[ASRProvider] = field(
        default_factory=lambda: [
            ASRProvider.DEEPGRAM,
            ASRProvider.GOOGLE,
            ASRProvider.BHASHINI,
        ]
    )
    min_audio_bytes: int = 200
    request_timeout_seconds: float = 15.0


class MultiProviderASR:
    """Speech-to-text with automatic fallback across Deepgram, Google, and Bhashini.

    On any provider failure or empty result, the next provider in the chain is tried
    automatically. If all fail, a structured error is returned (never raises).
    """

    def __init__(self, config: ASRConfig | None = None) -> None:
        self.config = config or ASRConfig()
        self._http = httpx.AsyncClient(timeout=self.config.request_timeout_seconds)

    async def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "hi",
        sample_rate: int = 16000,
    ) -> ASRResult:
        if not audio_bytes or len(audio_bytes) < self.config.min_audio_bytes:
            return ASRResult(error="audio_too_short")

        providers = self._available_providers()
        if not providers:
            logger.warning("asr_no_providers_configured, using mock")
            return self._mock_transcribe(language)

        last_error = ""
        for provider in providers:
            try:
                result = await self._dispatch(provider, audio_bytes, language, sample_rate)
                if result.success:
                    result.provider_used = provider.value
                    logger.info(
                        "asr_ok",
                        provider=provider.value,
                        lang=language,
                        confidence=round(result.confidence, 2),
                        text_len=len(result.text),
                    )
                    return result
                last_error = f"{provider.value}: empty_transcription"
            except Exception as exc:
                last_error = f"{provider.value}: {exc}"
                logger.warning("asr_fail", provider=provider.value, error=str(exc))

        logger.error("asr_all_failed", last_error=last_error)
        return ASRResult(error=f"All providers failed. Last: {last_error}")

    # ---- Provider dispatch ----

    async def _dispatch(
        self, provider: ASRProvider, audio: bytes, lang: str, rate: int,
    ) -> ASRResult:
        if provider == ASRProvider.DEEPGRAM:
            return await self._deepgram(audio, lang, rate)
        if provider == ASRProvider.GOOGLE:
            return await self._google(audio, lang, rate)
        if provider == ASRProvider.BHASHINI:
            return await self._bhashini(audio, lang, rate)
        return ASRResult(error=f"unknown_provider:{provider}")

    # ---- Deepgram: primary, lowest latency, $0.0043/min ----

    async def _deepgram(self, audio: bytes, lang: str, rate: int) -> ASRResult:
        dg_lang = LANGUAGE_CODES["deepgram"].get(lang, "hi")
        resp = await self._http.post(
            "https://api.deepgram.com/v1/listen",
            content=audio,
            headers={
                "Authorization": f"Token {self.config.deepgram_api_key}",
                "Content-Type": f"audio/l16;rate={rate}",
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

        channel = data.get("results", {}).get("channels", [{}])[0]
        alt = channel.get("alternatives", [{}])[0]
        duration = data.get("metadata", {}).get("duration", 0)

        return ASRResult(
            text=alt.get("transcript", ""),
            language_detected=lang,
            confidence=alt.get("confidence", 0.0),
            alternatives=[
                a.get("transcript", "")
                for a in channel.get("alternatives", [])[1:4]
            ],
            duration_ms=int(duration * 1000),
        )

    # ---- Google Speech-to-Text: fallback 1, widest lang support, $0.024/min ----

    async def _google(self, audio: bytes, lang: str, rate: int) -> ASRResult:
        g_lang = LANGUAGE_CODES["google"].get(lang, "hi-IN")
        audio_b64 = base64.b64encode(audio).decode()

        resp = await self._http.post(
            f"https://speech.googleapis.com/v1/speech:recognize?key={self.config.google_api_key}",
            json={
                "config": {
                    "encoding": "LINEAR16",
                    "sampleRateHertz": rate,
                    "languageCode": g_lang,
                    "model": "latest_long",
                    "enableAutomaticPunctuation": True,
                    "maxAlternatives": 3,
                },
                "audio": {"content": audio_b64},
            },
        )
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            return ASRResult(text="", language_detected=lang)

        best = results[0].get("alternatives", [{}])[0]
        return ASRResult(
            text=best.get("transcript", ""),
            language_detected=lang,
            confidence=best.get("confidence", 0.0),
            alternatives=[
                a.get("transcript", "")
                for r in results
                for a in r.get("alternatives", [])[1:4]
            ],
        )

    # ---- Bhashini: fallback 2, government/free, 22 Indian languages ----

    async def _bhashini(self, audio: bytes, lang: str, rate: int) -> ASRResult:
        bh_lang = LANGUAGE_CODES["bhashini"].get(lang, "hi")
        audio_b64 = base64.b64encode(audio).decode()

        # Step 1: fetch pipeline config
        pipe_resp = await self._http.post(
            "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline",
            json={
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {"language": {"sourceLanguage": bh_lang}},
                    }
                ],
                "pipelineRequestConfig": {
                    "pipelineId": self.config.bhashini_pipeline_id,
                },
            },
            headers={
                "ulcaApiKey": self.config.bhashini_api_key,
                "userID": self.config.bhashini_user_id,
            },
        )
        pipe_resp.raise_for_status()
        pipe = pipe_resp.json()

        ep = pipe.get("pipelineInferenceAPIEndPoint", {})
        callback_url = ep.get("callbackUrl", "")
        auth_value = ep.get("inferenceApiKey", {}).get("value", "")

        service_id = ""
        for tc in pipe.get("pipelineResponseConfig", []):
            if tc.get("taskType") == "asr":
                cfgs = tc.get("config", [])
                if cfgs:
                    service_id = cfgs[0].get("serviceId", "")
                break

        if not callback_url:
            return ASRResult(error="bhashini_no_callback_url")

        # Step 2: inference
        inf_resp = await self._http.post(
            callback_url,
            json={
                "pipelineTasks": [
                    {
                        "taskType": "asr",
                        "config": {
                            "language": {"sourceLanguage": bh_lang},
                            "serviceId": service_id,
                            "audioFormat": "wav",
                            "samplingRate": rate,
                        },
                    }
                ],
                "inputData": {"audio": [{"audioContent": audio_b64}]},
            },
            headers={
                "Authorization": auth_value,
                "Content-Type": "application/json",
            },
        )
        inf_resp.raise_for_status()
        inf = inf_resp.json()

        outputs = inf.get("pipelineResponse", [{}])[0].get("output", [])
        text = outputs[0].get("source", "") if outputs else ""

        return ASRResult(
            text=text,
            language_detected=lang,
            confidence=0.80 if text else 0.0,
        )

    # ---- Helpers ----

    def _available_providers(self) -> list[ASRProvider]:
        out = []
        for p in self.config.fallback_order:
            if (
                (p == ASRProvider.DEEPGRAM and self.config.deepgram_api_key)
                or (p == ASRProvider.GOOGLE and self.config.google_api_key)
                or (p == ASRProvider.BHASHINI and self.config.bhashini_api_key)
            ):
                out.append(p)
        return out

    def _mock_transcribe(self, language: str) -> ASRResult:
        return ASRResult(
            text=MOCK_TEXTS.get(language, MOCK_TEXTS["hi"]),
            language_detected=language,
            confidence=0.92,
            provider_used="mock",
        )

    async def close(self) -> None:
        await self._http.aclose()
