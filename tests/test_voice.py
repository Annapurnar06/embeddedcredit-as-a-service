"""Tests for Cartesia voice AI integration -- TTS, STT, and voice channel."""

import pytest

from app.voice.cartesia_client import (
    CartesiaSTTClient,
    CartesiaTTSClient,
    VoiceConfig,
    get_voice_for_segment,
)
from app.voice.voice_channel import VoiceChannel


class TestCartesiaTTSClient:
    @pytest.fixture
    def tts(self):
        return CartesiaTTSClient(api_key="")

    @pytest.mark.asyncio
    async def test_mock_synthesize(self, tts):
        result = await tts.synthesize("Namaste, main aapki madad karne ke liye yahan hoon.")
        assert result.audio_bytes
        assert len(result.audio_bytes) > 0
        assert result.duration_ms > 0
        assert result.error is None

    @pytest.mark.asyncio
    async def test_synthesize_with_config(self, tts):
        config = VoiceConfig(language="hi", speed=0.9)
        result = await tts.synthesize("Hello", config)
        assert result.audio_bytes
        assert result.error is None

    @pytest.mark.asyncio
    async def test_empty_text_synthesize(self, tts):
        result = await tts.synthesize("")
        assert result.error is None


class TestCartesiaSTTClient:
    @pytest.fixture
    def stt(self):
        return CartesiaSTTClient(api_key="")

    @pytest.mark.asyncio
    async def test_mock_transcribe_hindi(self, stt):
        result = await stt.transcribe(b"\x00\x00" * 1000, language="hi")
        assert result.text
        assert "loan" in result.text.lower() or "namaste" in result.text.lower()
        assert result.confidence > 0.5
        assert result.error is None

    @pytest.mark.asyncio
    async def test_mock_transcribe_english(self, stt):
        result = await stt.transcribe(b"\x00\x00" * 1000, language="en")
        assert result.text
        assert result.error is None


class TestVoiceConfig:
    def test_resolve_voice_id_default(self):
        config = VoiceConfig(language="hi")
        vid = config.resolve_voice_id("male")
        assert vid

    def test_resolve_voice_id_custom(self):
        config = VoiceConfig(voice_id="custom-123")
        assert config.resolve_voice_id() == "custom-123"

    def test_get_voice_for_segment_empathetic(self):
        config = get_voice_for_segment("SHG_MEMBER", "hi")
        assert config.emotion == "warm"
        assert config.speed == 0.9

    def test_get_voice_for_segment_professional(self):
        config = get_voice_for_segment("FPO_ENTITY", "en")
        assert config.emotion == "professional"
        assert config.speed == 1.0

    def test_get_voice_for_segment_default(self):
        config = get_voice_for_segment("DAIRY_FARMER", "hi")
        assert config.emotion == "neutral"


class TestVoiceChannel:
    @pytest.fixture
    def channel(self):
        return VoiceChannel()

    @pytest.mark.asyncio
    async def test_start_call(self, channel):
        result = await channel.start_call(
            channel_user_id="9876543210",
            lender_id="TEST_LENDER",
            language="hi",
            segment="DAIRY_FARMER",
        )
        assert "call_id" in result
        assert "session_id" in result
        assert "greeting_text" in result
        assert result["greeting_text"]

    @pytest.mark.asyncio
    async def test_full_call_flow(self, channel):
        start = await channel.start_call(
            channel_user_id="9876543210",
            lender_id="TEST_LENDER",
            language="hi",
        )
        call_id = start["call_id"]

        turn = await channel.process_audio_turn(call_id, b"\x00\x00" * 1000)
        assert turn["call_id"] == call_id
        assert "transcription" in turn
        assert "response_text" in turn

        summary = await channel.end_call(call_id)
        assert summary["call_id"] == call_id
        assert summary["total_turns"] == 1

    @pytest.mark.asyncio
    async def test_end_nonexistent_call(self, channel):
        result = await channel.end_call("nonexistent")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_process_turn_ended_call(self, channel):
        result = await channel.process_audio_turn("nonexistent", b"\x00\x00")
        assert "error" in result

    @pytest.mark.asyncio
    async def test_active_calls(self, channel):
        await channel.start_call("user1", "LENDER_A", "hi")
        await channel.start_call("user2", "LENDER_B", "en")
        calls = channel.get_active_calls()
        assert len(calls) == 2
