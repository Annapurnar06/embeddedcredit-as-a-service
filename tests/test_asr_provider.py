"""Tests for multi-provider ASR fallback chain."""

import pytest

from app.voice.asr_provider import ASRConfig, ASRProvider, ASRResult, MultiProviderASR


@pytest.fixture
def asr_no_keys():
    return MultiProviderASR(ASRConfig())


@pytest.fixture
def asr_deepgram_only():
    return MultiProviderASR(ASRConfig(deepgram_api_key="test_key"))


class TestASRResult:
    def test_success_property(self):
        r = ASRResult(text="hello", confidence=0.9)
        assert r.success is True

    def test_empty_not_success(self):
        r = ASRResult(text="", confidence=0.0)
        assert r.success is False

    def test_error_not_success(self):
        r = ASRResult(text="hello", error="some_error")
        assert r.success is False


class TestASRConfig:
    def test_default_fallback_order(self):
        c = ASRConfig()
        assert c.fallback_order == [ASRProvider.DEEPGRAM, ASRProvider.GOOGLE, ASRProvider.BHASHINI]

    def test_custom_order(self):
        c = ASRConfig(fallback_order=[ASRProvider.BHASHINI, ASRProvider.DEEPGRAM])
        assert c.fallback_order[0] == ASRProvider.BHASHINI


class TestMultiProviderASR:
    @pytest.mark.asyncio
    async def test_no_keys_returns_mock(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language="hi")
        assert result.success
        assert result.provider_used == "mock"
        assert "loan" in result.text.lower() or "namaste" in result.text.lower()

    @pytest.mark.asyncio
    async def test_mock_hindi(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language="hi")
        assert "loan" in result.text.lower()

    @pytest.mark.asyncio
    async def test_mock_gujarati(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language="gu")
        assert result.success
        assert result.language_detected == "gu"

    @pytest.mark.asyncio
    async def test_mock_tamil(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language="ta")
        assert result.success

    @pytest.mark.asyncio
    async def test_mock_all_languages(self, asr_no_keys):
        for lang in ["hi", "en", "gu", "ta", "te", "bn", "mr", "kn", "ml", "pa"]:
            result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language=lang)
            assert result.success, f"Failed for language {lang}"

    @pytest.mark.asyncio
    async def test_too_short_audio(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00", language="hi")
        assert not result.success
        assert result.error == "audio_too_short"

    @pytest.mark.asyncio
    async def test_empty_audio(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"", language="hi")
        assert result.error == "audio_too_short"

    @pytest.mark.asyncio
    async def test_available_providers_none(self, asr_no_keys):
        providers = asr_no_keys._available_providers()
        assert providers == []

    @pytest.mark.asyncio
    async def test_available_providers_deepgram(self, asr_deepgram_only):
        providers = asr_deepgram_only._available_providers()
        assert providers == [ASRProvider.DEEPGRAM]

    @pytest.mark.asyncio
    async def test_available_providers_all(self):
        asr = MultiProviderASR(ASRConfig(
            deepgram_api_key="dk",
            google_api_key="gk",
            bhashini_api_key="bk",
            bhashini_user_id="bu",
        ))
        providers = asr._available_providers()
        assert len(providers) == 3

    @pytest.mark.asyncio
    async def test_confidence_above_threshold(self, asr_no_keys):
        result = await asr_no_keys.transcribe(b"\x00\x00" * 200, language="hi")
        assert result.confidence > 0.5
