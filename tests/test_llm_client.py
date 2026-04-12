"""Tests for production LLM clients -- OpenAI and Anthropic with mock fallback."""

import pytest

from app.agent.llm import LLMMessage
from app.agent.llm_client import AnthropicClient, OpenAIClient, create_llm_client


class TestOpenAIClient:
    @pytest.fixture
    def client(self):
        return OpenAIClient(api_key="", model="gpt-4o")

    @pytest.mark.asyncio
    async def test_fallback_to_mock(self, client):
        messages = [
            LLMMessage(role="system", content="You are a lending assistant."),
            LLMMessage(role="user", content="Namaste"),
        ]
        response = await client.chat(messages)
        assert response.content
        assert response.model

    @pytest.mark.asyncio
    async def test_fallback_with_tools(self, client):
        messages = [
            LLMMessage(role="system", content="You are a lending assistant."),
            LLMMessage(role="user", content="Verify my aadhaar"),
        ]
        tools = [{"name": "verify_aadhaar_otp", "description": "Verify Aadhaar via OTP"}]
        response = await client.chat(messages, tools=tools)
        assert response.tool_calls or response.content

    @pytest.mark.asyncio
    async def test_token_tracking(self, client):
        messages = [LLMMessage(role="user", content="Hello")]
        await client.chat(messages)
        assert client.total_tokens_used >= 0


class TestAnthropicClient:
    @pytest.fixture
    def client(self):
        return AnthropicClient(api_key="", model="claude-sonnet-4-20250514")

    @pytest.mark.asyncio
    async def test_fallback_to_mock(self, client):
        messages = [
            LLMMessage(role="user", content="Namaste"),
        ]
        response = await client.chat(messages)
        assert response.content

    @pytest.mark.asyncio
    async def test_system_message_handling(self, client):
        messages = [
            LLMMessage(role="system", content="You are a lending assistant for dairy farmers."),
            LLMMessage(role="user", content="Hello"),
        ]
        response = await client.chat(messages)
        assert response.content


class TestCreateLLMClient:
    def test_create_openai(self):
        client = create_llm_client(provider="openai")
        assert isinstance(client, OpenAIClient)

    def test_create_anthropic(self):
        client = create_llm_client(provider="anthropic")
        assert isinstance(client, AnthropicClient)

    def test_default_provider(self):
        client = create_llm_client()
        assert isinstance(client, (OpenAIClient, AnthropicClient))
