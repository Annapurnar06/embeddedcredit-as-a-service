"""Tests for voice AI eval framework -- TTS evals, ASR evals, pipeline round-trip."""

import pytest

from app.voice.eval_framework import (
    ASREvaluator,
    EvalCase,
    EvalSuiteReport,
    LENDING_EVAL_CASES,
    PipelineEvaluator,
    TTSEvaluator,
)


class TestEvalCases:
    def test_builtin_cases_cover_languages(self):
        languages = {c.language for c in LENDING_EVAL_CASES}
        assert "hi" in languages
        assert "en" in languages
        assert "gu" in languages
        assert "ta" in languages
        assert len(languages) >= 6

    def test_builtin_cases_cover_segments(self):
        segments = {c.segment for c in LENDING_EVAL_CASES}
        assert "DAIRY_FARMER" in segments
        assert "GIG_WORKER" in segments
        assert len(segments) >= 5

    def test_builtin_cases_have_keywords(self):
        for case in LENDING_EVAL_CASES:
            assert case.expected_keywords, f"{case.case_id} has no keywords"

    def test_builtin_cases_have_intent(self):
        for case in LENDING_EVAL_CASES:
            assert case.expected_intent, f"{case.case_id} has no expected_intent"


class TestTTSEvaluator:
    @pytest.fixture
    def evaluator(self):
        return TTSEvaluator()

    @pytest.mark.asyncio
    async def test_eval_single_hindi(self, evaluator):
        case = EvalCase("test_hi", "hi", "DAIRY_FARMER", "Namaste, mujhe loan chahiye")
        result = await evaluator.eval_single(case)
        assert result.passed
        assert result.audio_bytes_len > 0
        assert result.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_eval_single_all_languages(self, evaluator):
        for lang in ["hi", "en", "gu", "ta", "te", "bn", "mr"]:
            case = EvalCase(f"test_{lang}", lang, "DAIRY_FARMER", "Test text for evaluation")
            result = await evaluator.eval_single(case)
            assert result.has_audio, f"TTS failed for {lang}: {result.error}"

    @pytest.mark.asyncio
    async def test_eval_suite(self, evaluator):
        report = await evaluator.eval_suite()
        assert report.total_cases == len(LENDING_EVAL_CASES)
        assert report.pass_rate > 0.8
        assert report.language_breakdown


class TestASREvaluator:
    @pytest.fixture
    def evaluator(self):
        return ASREvaluator()

    @pytest.mark.asyncio
    async def test_eval_mock_suite(self, evaluator):
        report = await evaluator.eval_suite_mock()
        assert report.total_cases == len(LENDING_EVAL_CASES)
        assert report.pass_rate > 0.8
        assert report.avg_latency_ms >= 0

    @pytest.mark.asyncio
    async def test_eval_single_mock(self, evaluator):
        case = EvalCase(
            "test_asr_hi", "hi", "DAIRY_FARMER",
            "Namaste mujhe loan chahiye",
            expected_keywords=["loan", "namaste"],
        )
        mock_audio = b"\x00\x80" * 8000
        result = await evaluator.eval_single(case, mock_audio)
        assert result.passed
        assert result.confidence > 0.5


class TestPipelineEvaluator:
    @pytest.fixture
    def evaluator(self):
        return PipelineEvaluator()

    @pytest.mark.asyncio
    async def test_round_trip_hindi(self, evaluator):
        case = EvalCase(
            "rt_hi", "hi", "DAIRY_FARMER",
            "Namaste, mujhe loan chahiye",
            expected_keywords=["loan"],
            expected_intent="loan_inquiry",
        )
        result = await evaluator.eval_round_trip(case)
        assert result.tts_result is not None
        assert result.asr_result is not None
        assert result.round_trip_ms >= 0

    @pytest.mark.asyncio
    async def test_intent_classification(self, evaluator):
        assert evaluator._classify_intent("mujhe loan chahiye", "hi") == "loan_inquiry"
        assert evaluator._classify_intent("EMI kab hai", "hi") == "repayment_status"
        assert evaluator._classify_intent("shikayat karna hai", "hi") == "complaint"
        assert evaluator._classify_intent("baarish se pareshani", "hi") == "emergency"
        assert evaluator._classify_intent("namaste", "hi") == "general"

    @pytest.mark.asyncio
    async def test_pipeline_suite(self, evaluator):
        cases = LENDING_EVAL_CASES[:3]
        report = await evaluator.eval_suite(cases)
        assert report.total_cases == 3
        assert report.suite_name == "pipeline_eval"
        assert report.language_breakdown
        assert report.segment_breakdown


class TestEvalSuiteReport:
    def test_pass_rate_calculation(self):
        r = EvalSuiteReport(suite_name="test", total_cases=10, passed=7, failed=3)
        assert r.pass_rate == 0.7

    def test_to_dict(self):
        r = EvalSuiteReport(suite_name="test", total_cases=5, passed=4, failed=1)
        d = r.to_dict()
        assert d["suite_name"] == "test"
        assert d["pass_rate"] == 0.8
        assert "language_breakdown" in d

    def test_empty_report(self):
        r = EvalSuiteReport(suite_name="empty")
        assert r.pass_rate == 0.0
