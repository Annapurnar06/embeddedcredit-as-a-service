"""Production LLM client -- OpenAI and Anthropic with token budget management."""

from __future__ import annotations

import contextlib
import json
from typing import Any

import httpx

from app.agent.llm import LLMMessage, LLMResponse, ToolCall
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_FALLBACK_MSG = "Main abhi jawab nahi de pa raha. Kripya thodi der baad koshish karein."


class OpenAIClient:
    """Production OpenAI client with structured tool calling."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o",
        max_tokens: int = 1024,
    ) -> None:
        self.api_key = api_key or settings.openai_api_key
        self.model = model
        self.max_tokens = max_tokens
        self._http = httpx.AsyncClient(timeout=60.0)
        self._total_tokens = 0

    async def chat(
        self,
        messages: list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.3,
    ) -> LLMResponse:
        if not self.api_key:
            from app.agent.llm import MockLLMClient

            mock = MockLLMClient(model=self.model)
            return await mock.chat(messages, tools, temperature)

        openai_messages = [{"role": m.role, "content": m.content} for m in messages]

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": temperature,
            "max_tokens": self.max_tokens,
        }

        if tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t.get("description", ""),
                        "parameters": t.get("parameters", {"type": "object", "properties": {}}),
                    },
                }
                for t in tools
            ]
            payload["tool_choice"] = "auto"

        try:
            resp = await self._http.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            choice = data["choices"][0]
            message = choice["message"]
            usage = data.get("usage", {})
            self._total_tokens += usage.get("total_tokens", 0)

            tool_calls = []
            if message.get("tool_calls"):
                for tc in message["tool_calls"]:
                    fn = tc["function"]
                    args = {}
                    with contextlib.suppress(json.JSONDecodeError):
                        args = json.loads(fn.get("arguments", "{}"))
                    tool_calls.append(ToolCall(tool_name=fn["name"], arguments=args))

            logger.info(
                "openai_chat_complete",
                model=self.model,
                prompt_tokens=usage.get("prompt_tokens", 0),
                completion_tokens=usage.get("completion_tokens", 0),
                tool_calls=len(tool_calls),
            )

            return LLMResponse(
                content=message.get("content", "") or "",
                tool_calls=tool_calls,
                finish_reason=choice.get("finish_reason", "stop"),
                model=data.get("model", self.model),
                usage=usage,
            )
        except httpx.HTTPStatusError as e:
            logger.error(
                "openai_error",
                status=e.response.status_code,
                body=e.response.text[:500],
            )
            return LLMResponse(content=_FALLBACK_MSG)
        except Exception as e:
            logger.error("openai_exception", error=str(e))
            return LLMResponse(content=_FALLBACK_MSG)

    @property
    def total_tokens_used(self) -> int:
        return self._total_tokens

    async def close(self) -> None:
        await self._http.aclose()


class AnthropicClient:
    """Production Anthropic client with tool use support."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 1024,
    ) -> None:
        self.api_key = api_key or settings.anthropic_api_key
        self.model = model
        self.max_tokens = max_tokens
        self._http = httpx.AsyncClient(timeout=60.0)
        self._total_tokens = 0

    async def chat(
        self,
        messages: list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.3,
    ) -> LLMResponse:
        if not self.api_key:
            from app.agent.llm import MockLLMClient

            mock = MockLLMClient(model=self.model)
            return await mock.chat(messages, tools, temperature)

        system_msg = ""
        anthropic_messages = []
        for m in messages:
            if m.role == "system":
                system_msg += m.content + "\n"
            else:
                anthropic_messages.append({"role": m.role, "content": m.content})

        if not anthropic_messages:
            anthropic_messages = [{"role": "user", "content": "Hello"}]

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "messages": anthropic_messages,
            "temperature": temperature,
        }
        if system_msg:
            payload["system"] = system_msg.strip()

        if tools:
            payload["tools"] = [
                {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "input_schema": t.get("parameters", {"type": "object", "properties": {}}),
                }
                for t in tools
            ]

        try:
            resp = await self._http.post(
                "https://api.anthropic.com/v1/messages",
                json=payload,
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            content_text = ""
            tool_calls = []
            for block in data.get("content", []):
                if block["type"] == "text":
                    content_text += block["text"]
                elif block["type"] == "tool_use":
                    tool_calls.append(
                        ToolCall(
                            tool_name=block["name"],
                            arguments=block.get("input", {}),
                        )
                    )

            usage = data.get("usage", {})
            self._total_tokens += usage.get("input_tokens", 0) + usage.get("output_tokens", 0)

            logger.info(
                "anthropic_chat_complete",
                model=self.model,
                input_tokens=usage.get("input_tokens", 0),
                output_tokens=usage.get("output_tokens", 0),
                tool_calls=len(tool_calls),
            )

            return LLMResponse(
                content=content_text,
                tool_calls=tool_calls,
                finish_reason=data.get("stop_reason", "end_turn"),
                model=data.get("model", self.model),
                usage=usage,
            )
        except httpx.HTTPStatusError as e:
            logger.error(
                "anthropic_error",
                status=e.response.status_code,
                body=e.response.text[:500],
            )
            return LLMResponse(content=_FALLBACK_MSG)
        except Exception as e:
            logger.error("anthropic_exception", error=str(e))
            return LLMResponse(content=_FALLBACK_MSG)

    @property
    def total_tokens_used(self) -> int:
        return self._total_tokens

    async def close(self) -> None:
        await self._http.aclose()


def create_llm_client(
    provider: str | None = None,
    model: str | None = None,
) -> OpenAIClient | AnthropicClient:
    prov = provider or settings.llm_provider
    if prov == "anthropic":
        return AnthropicClient(model=model or "claude-sonnet-4-20250514")
    return OpenAIClient(model=model or "gpt-4o")
