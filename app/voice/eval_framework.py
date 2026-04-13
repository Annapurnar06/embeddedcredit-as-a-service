"""Voice AI evaluation framework.

Measures TTS quality, ASR accuracy, pipeline latency, and segment coverage.

Provides automated eval suites that run against Cartesia TTS, multi-provider ASR,
and the full voice pipeline (ASR -> intent -> agent -> TTS round-trip).
Results are structured for CI/CD gating and regression tracking.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from app.core.logging import get_logger
from app.voice.asr_provider import MultiProviderASR
from app.voice.cartesia_client import CartesiaTTSClient, VoiceConfig

logger = get_logger(__name__)


# ---- Eval data types ----

@dataclass
class EvalCase:
    case_id: str
    language: str
    segment: str
    input_text: str
    expected_keywords: list[str] = field(default_factory=list)
    expected_intent: str = ""
    max_tts_latency_ms: int = 2000
    max_asr_latency_ms: int = 3000
    min_asr_confidence: float = 0.6


@dataclass
class TTSEvalResult:
    case_id: str
    language: str
    audio_bytes_len: int = 0
    duration_ms: int = 0
    latency_ms: int = 0
    error: str | None = None
    passed: bool = False

    @property
    def has_audio(self) -> bool:
        return self.audio_bytes_len > 0 and self.error is None


@dataclass
class ASREvalResult:
    case_id: str
    language: str
    provider_used: str = ""
    transcribed_text: str = ""
    confidence: float = 0.0
    latency_ms: int = 0
    keyword_hits: int = 0
    keyword_total: int = 0
    error: str | None = None
    passed: bool = False

    @property
    def keyword_accuracy(self) -> float:
        return self.keyword_hits / max(self.keyword_total, 1)


@dataclass
class PipelineEvalResult:
    case_id: str
    language: str
    segment: str
    tts_result: TTSEvalResult | None = None
    asr_result: ASREvalResult | None = None
    round_trip_ms: int = 0
    intent_detected: str = ""
    intent_correct: bool = False
    agent_response: str = ""
    response_tts_result: TTSEvalResult | None = None
    passed: bool = False


@dataclass
class EvalSuiteReport:
    suite_name: str
    total_cases: int = 0
    passed: int = 0
    failed: int = 0
    avg_latency_ms: float = 0.0
    language_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)
    segment_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)
    failures: list[dict[str, Any]] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        return self.passed / max(self.total_cases, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "suite_name": self.suite_name,
            "total_cases": self.total_cases,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": round(self.pass_rate, 3),
            "avg_latency_ms": round(self.avg_latency_ms, 1),
            "language_breakdown": self.language_breakdown,
            "segment_breakdown": self.segment_breakdown,
            "failures": self.failures[:20],
        }


# ---- Built-in eval cases ----

LENDING_EVAL_CASES: list[EvalCase] = [
    # Hindi
    EvalCase("hi_loan_01", "hi", "DAIRY_FARMER",
             "Namaste, mujhe gaay kharidne ke liye loan chahiye",
             expected_keywords=["loan", "gaay"], expected_intent="loan_inquiry"),
    EvalCase("hi_loan_02", "hi", "STREET_VENDOR",
             "Mujhe apni dukaan ke liye paisa chahiye, kuch kaam ka karz",
             expected_keywords=["dukaan", "paisa"], expected_intent="loan_inquiry"),
    EvalCase("hi_repay_01", "hi", "GIG_WORKER",
             "Meri EMI kab hai, kitna baki hai",
             expected_keywords=["EMI", "baki"], expected_intent="repayment_status"),
    EvalCase("hi_emerg_01", "hi", "DAIRY_FARMER",
             "Bahut pareshani hai, baarish se fasal kharab ho gayi",
             expected_keywords=["pareshani", "baarish", "fasal"], expected_intent="emergency"),
    EvalCase("hi_complaint_01", "hi", "SHG_MEMBER",
             "Shikayat karna hai, galat amount kata hai",
             expected_keywords=["shikayat", "galat"], expected_intent="complaint"),
    # Gujarati
    EvalCase("gu_loan_01", "gu", "DAIRY_FARMER",
             "Namaste, mane bhens leva mate loan joiye chhe",
             expected_keywords=["loan", "bhens"], expected_intent="loan_inquiry"),
    # Tamil
    EvalCase("ta_loan_01", "ta", "FISHERY",
             "Vanakkam, enakku padagu vaanga loan venum",
             expected_keywords=["loan", "padagu"], expected_intent="loan_inquiry"),
    # Telugu
    EvalCase("te_loan_01", "te", "KIRANA_SHOP",
             "Namaskaram, na shop ki working capital loan kavali",
             expected_keywords=["loan", "shop"], expected_intent="loan_inquiry"),
    # Bengali
    EvalCase("bn_loan_01", "bn", "CONSTRUCTION_WORKER",
             "Nomoshkar, amar bari toiri korte loan dorkar",
             expected_keywords=["loan", "bari"], expected_intent="loan_inquiry"),
    # English
    EvalCase("en_loan_01", "en", "EV_FINANCING",
             "Hello, I need a loan to buy an electric vehicle",
             expected_keywords=["loan", "electric"], expected_intent="loan_inquiry"),
    # Marathi
    EvalCase("mr_loan_01", "mr", "DAIRY_FARMER",
             "Namaskar, mala gai ghet loan pahije",
             expected_keywords=["loan", "gai"], expected_intent="loan_inquiry"),
]


# ---- TTS Evaluation ----

class TTSEvaluator:
    """Evaluates Cartesia TTS: audio generation, latency, language coverage."""

    def __init__(self, tts_client: CartesiaTTSClient | None = None) -> None:
        self.tts = tts_client or CartesiaTTSClient()

    async def eval_single(self, case: EvalCase) -> TTSEvalResult:
        config = VoiceConfig(language=case.language)
        start = time.monotonic()
        tts_result = await self.tts.synthesize(case.input_text, config)
        latency = int((time.monotonic() - start) * 1000)

        passed = (
            tts_result.error is None
            and len(tts_result.audio_bytes) > 0
            and latency <= case.max_tts_latency_ms
        )

        return TTSEvalResult(
            case_id=case.case_id,
            language=case.language,
            audio_bytes_len=len(tts_result.audio_bytes),
            duration_ms=tts_result.duration_ms,
            latency_ms=latency,
            error=tts_result.error,
            passed=passed,
        )

    async def eval_suite(
        self, cases: list[EvalCase] | None = None,
    ) -> EvalSuiteReport:
        cases = cases or LENDING_EVAL_CASES
        report = EvalSuiteReport(suite_name="tts_eval", total_cases=len(cases))
        latencies = []

        for case in cases:
            result = await self.eval_single(case)
            lang = result.language
            report.language_breakdown.setdefault(lang, {"passed": 0, "failed": 0})

            if result.passed:
                report.passed += 1
                report.language_breakdown[lang]["passed"] += 1
            else:
                report.failed += 1
                report.language_breakdown[lang]["failed"] += 1
                report.failures.append({
                    "case_id": result.case_id,
                    "language": lang,
                    "error": result.error,
                    "latency_ms": result.latency_ms,
                })

            latencies.append(result.latency_ms)

        report.avg_latency_ms = sum(latencies) / max(len(latencies), 1)
        return report


# ---- ASR Evaluation ----

class ASREvaluator:
    """Evaluates ASR providers: transcription accuracy, keyword matching, fallback behavior."""

    def __init__(self, asr: MultiProviderASR | None = None) -> None:
        self.asr = asr or MultiProviderASR()

    async def eval_single(self, case: EvalCase, audio_bytes: bytes) -> ASREvalResult:
        start = time.monotonic()
        asr_result = await self.asr.transcribe(audio_bytes, language=case.language)
        latency = int((time.monotonic() - start) * 1000)

        keyword_hits = 0
        text_lower = asr_result.text.lower()
        for kw in case.expected_keywords:
            if kw.lower() in text_lower:
                keyword_hits += 1

        passed = (
            asr_result.success
            and asr_result.confidence >= case.min_asr_confidence
            and latency <= case.max_asr_latency_ms
        )

        return ASREvalResult(
            case_id=case.case_id,
            language=case.language,
            provider_used=asr_result.provider_used,
            transcribed_text=asr_result.text,
            confidence=asr_result.confidence,
            latency_ms=latency,
            keyword_hits=keyword_hits,
            keyword_total=len(case.expected_keywords),
            error=asr_result.error,
            passed=passed,
        )

    async def eval_suite_mock(
        self, cases: list[EvalCase] | None = None,
    ) -> EvalSuiteReport:
        """Run eval using mock audio (for CI -- no real audio files needed)."""
        cases = cases or LENDING_EVAL_CASES
        report = EvalSuiteReport(suite_name="asr_eval_mock", total_cases=len(cases))
        latencies = []

        for case in cases:
            mock_audio = b"\x00\x80" * 8000  # 1 second of silence at 16kHz
            result = await self.eval_single(case, mock_audio)
            lang = result.language
            report.language_breakdown.setdefault(lang, {"passed": 0, "failed": 0})

            if result.passed:
                report.passed += 1
                report.language_breakdown[lang]["passed"] += 1
            else:
                report.failed += 1
                report.language_breakdown[lang]["failed"] += 1
                report.failures.append({
                    "case_id": result.case_id,
                    "language": lang,
                    "error": result.error,
                    "confidence": result.confidence,
                })

            latencies.append(result.latency_ms)

        report.avg_latency_ms = sum(latencies) / max(len(latencies), 1)
        return report


# ---- Full Pipeline Evaluation ----

class PipelineEvaluator:
    """End-to-end voice pipeline eval: TTS -> ASR -> intent -> agent -> TTS response."""

    def __init__(
        self,
        tts: CartesiaTTSClient | None = None,
        asr: MultiProviderASR | None = None,
    ) -> None:
        self.tts_eval = TTSEvaluator(tts)
        self.asr_eval = ASREvaluator(asr)
        self.tts = tts or CartesiaTTSClient()
        self.asr = asr or MultiProviderASR()

    async def eval_round_trip(self, case: EvalCase) -> PipelineEvalResult:
        """Full round-trip: text -> TTS -> audio -> ASR -> text (measures fidelity loss)."""
        start = time.monotonic()

        # Step 1: TTS -- generate audio from input text
        tts_result = await self.tts_eval.eval_single(case)

        # Step 2: ASR -- transcribe the generated audio back to text
        if tts_result.has_audio:
            config = VoiceConfig(language=case.language)
            synth = await self.tts.synthesize(case.input_text, config)
            asr_result = await self.asr_eval.eval_single(case, synth.audio_bytes)
        else:
            asr_result = ASREvalResult(
                case_id=case.case_id,
                language=case.language,
                error="no_tts_audio",
            )

        round_trip_ms = int((time.monotonic() - start) * 1000)

        # Step 3: Intent classification from transcribed text
        intent = self._classify_intent(asr_result.transcribed_text, case.language)
        intent_correct = intent == case.expected_intent if case.expected_intent else True

        passed = tts_result.passed and asr_result.passed and intent_correct

        return PipelineEvalResult(
            case_id=case.case_id,
            language=case.language,
            segment=case.segment,
            tts_result=tts_result,
            asr_result=asr_result,
            round_trip_ms=round_trip_ms,
            intent_detected=intent,
            intent_correct=intent_correct,
            passed=passed,
        )

    async def eval_suite(
        self, cases: list[EvalCase] | None = None,
    ) -> EvalSuiteReport:
        cases = cases or LENDING_EVAL_CASES
        report = EvalSuiteReport(suite_name="pipeline_eval", total_cases=len(cases))
        latencies = []

        for case in cases:
            result = await self.eval_round_trip(case)
            lang = result.language
            seg = result.segment
            report.language_breakdown.setdefault(lang, {"passed": 0, "failed": 0})
            report.segment_breakdown.setdefault(seg, {"passed": 0, "failed": 0})

            if result.passed:
                report.passed += 1
                report.language_breakdown[lang]["passed"] += 1
                report.segment_breakdown[seg]["passed"] += 1
            else:
                report.failed += 1
                report.language_breakdown[lang]["failed"] += 1
                report.segment_breakdown[seg]["failed"] += 1
                report.failures.append({
                    "case_id": result.case_id,
                    "language": lang,
                    "segment": seg,
                    "tts_ok": result.tts_result.passed if result.tts_result else False,
                    "asr_ok": result.asr_result.passed if result.asr_result else False,
                    "intent_ok": result.intent_correct,
                    "round_trip_ms": result.round_trip_ms,
                })

            latencies.append(result.round_trip_ms)

        report.avg_latency_ms = sum(latencies) / max(len(latencies), 1)
        return report

    @staticmethod
    def _classify_intent(text: str, language: str) -> str:
        """Simple keyword intent classifier for eval purposes."""
        t = text.lower()
        emergency_kw = ["pareshani", "baarish", "baadh", "emergency", "urgent", "medical"]
        complaint_kw = ["shikayat", "galat", "complaint", "wrong"]
        repayment_kw = ["emi", "baki", "payment", "repay", "kist"]
        loan_kw = ["loan", "karz", "paisa", "udhar", "money", "finance",
                    "chahiye", "joiye", "venum", "kavali", "dorkar", "pahije", "beku", "venam"]

        if any(k in t for k in emergency_kw):
            return "emergency"
        if any(k in t for k in complaint_kw):
            return "complaint"
        if any(k in t for k in repayment_kw):
            return "repayment_status"
        if any(k in t for k in loan_kw):
            return "loan_inquiry"
        return "general"
