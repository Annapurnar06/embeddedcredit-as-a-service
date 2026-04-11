"""LLM client abstraction -- single provider (OpenAI) with structured output."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LLMMessage:
    role: str
    content: str


@dataclass
class ToolCall:
    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass
class LLMResponse:
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    finish_reason: str = "stop"
    model: str = ""
    usage: dict[str, int] = field(default_factory=dict)


class MockLLMClient:
    """Mock LLM client for testing without API keys.

    Implements the same interface as a real OpenAI client.
    Routes based on conversation context to simulate realistic agent behavior.
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        self.model = model
        self._call_count = 0

    async def chat(
        self,
        messages: list[LLMMessage],
        tools: list[dict[str, Any]] | None = None,
        temperature: float = 0.3,
    ) -> LLMResponse:
        self._call_count += 1
        last_user = ""
        for msg in reversed(messages):
            if msg.role == "user":
                last_user = msg.content.lower()
                break

        if tools and self._should_call_tool(last_user, messages):
            return self._route_tool_call(last_user, messages)

        return LLMResponse(
            content=self._generate_response(last_user, messages),
            model=self.model,
            usage={"prompt_tokens": 100, "completion_tokens": 50},
        )

    def _should_call_tool(self, user_msg: str, messages: list[LLMMessage]) -> bool:
        tool_triggers = [
            "aadhaar", "verify", "loan", "apply", "check", "status",
            "payment", "emi", "moratorium", "score", "bureau",
        ]
        return any(t in user_msg for t in tool_triggers)

    def _route_tool_call(
        self, user_msg: str, messages: list[LLMMessage]
    ) -> LLMResponse:
        if any(w in user_msg for w in ["aadhaar", "verify", "kyc"]):
            return LLMResponse(
                tool_calls=[ToolCall(
                    tool_name="verify_aadhaar_otp",
                    arguments={"aadhaar_number": "123456789012"},
                )],
                finish_reason="tool_calls",
                model=self.model,
            )

        if any(w in user_msg for w in ["pan"]):
            return LLMResponse(
                tool_calls=[ToolCall(
                    tool_name="verify_pan",
                    arguments={"pan_number": "ABCDE1234F", "aadhaar_name": "Ramesh Patel"},
                )],
                finish_reason="tool_calls",
                model=self.model,
            )

        if any(w in user_msg for w in ["loan", "apply", "rin", "karz"]):
            return LLMResponse(
                content="Loan ke liye pehle aapki pehchaan verify karni hogi. "
                "Kya aap apna Aadhaar number bata sakte hain?",
                model=self.model,
            )

        if any(w in user_msg for w in ["status", "check"]):
            return LLMResponse(
                tool_calls=[ToolCall(
                    tool_name="get_loan_status",
                    arguments={},
                )],
                finish_reason="tool_calls",
                model=self.model,
            )

        return LLMResponse(
            content=(
                "Main aapki madad karne ke liye yahan hoon. "
                "Kya aap batayenge ki aapko kis cheez mein madad chahiye?"
            ),
            model=self.model,
        )

    def _generate_response(self, user_msg: str, messages: list[LLMMessage]) -> str:
        if any(w in user_msg for w in ["namaste", "hello", "hi"]):
            return (
                "Namaste! Main aapki madad karne ke liye yahan hoon. "
                "Kya aap loan ke baare mein jaanna chahte hain?"
            )

        if any(w in user_msg for w in ["haan", "yes", "theek", "confirm"]):
            return "Dhanyavaad. Aage badhte hain."

        if any(w in user_msg for w in ["nahi", "no", "nah"]):
            return "Theek hai. Kya aur kuch madad chahiye?"

        if any(w in user_msg for w in ["death", "died", "bimari", "flood"]):
            return (
                "Mujhe bahut dukh hua yeh sunkar. Hum aapki mushkil samajhte hain. "
                "Hum aapke loan mein moratorium ka intezaam kar sakte hain."
            )

        if any(w in user_msg for w in ["complaint", "shikayat", "wrong"]):
            return (
                "Main samajhta hoon aapki pareshani. Aap hamare grievance officer "
                "se sampark kar sakte hain. Unka number hai..."
            )

        return "Main samajh gaya. Kya aur koi sawal hai?"
