"""Agent runtime -- orchestrates conversation, tool calling, and behavioral supervision."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any

from app.agent.confirmation import detect_confirmation
from app.agent.llm import LLMMessage, MockLLMClient, ToolCall
from app.agent.prompts import build_system_prompt, build_tool_result_prompt
from app.core.audit import AuditTrail, EventEmitter
from app.core.logging import get_logger
from app.models.session import SessionState
from app.policy.behavioral import BehavioralContext
from app.policy.engine import PolicyEngine
from app.segments.loader import SegmentRegistry
from app.tools.executor import ExecutionContext, ToolExecutor, ToolResult
from app.tools.registry import ToolRegistry, ToolResultStatus
from app.tools.session_machine import SessionMachine

logger = get_logger(__name__)


@dataclass
class ConversationTurn:
    borrower_message: str
    agent_response: str
    tools_called: list[str] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    state_before: str = ""
    state_after: str = ""


@dataclass
class AgentSession:
    session_id: uuid.UUID
    lender_id: str
    state: SessionState = SessionState.UNVERIFIED
    segment: str | None = None
    language: str = "hi"
    borrower_id: uuid.UUID | None = None
    loan_application_id: uuid.UUID | None = None
    history: list[ConversationTurn] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    kfs_generated: bool = False
    maker_approved: bool = False

    @property
    def messages(self) -> list[LLMMessage]:
        msgs: list[LLMMessage] = []
        for turn in self.history[-10:]:
            msgs.append(LLMMessage(role="user", content=turn.borrower_message))
            msgs.append(LLMMessage(role="assistant", content=turn.agent_response))
        return msgs


class AgentRuntime:
    def __init__(
        self,
        llm_client: MockLLMClient | None = None,
        policy_engine: PolicyEngine | None = None,
        tool_executor: ToolExecutor | None = None,
        audit_trail: AuditTrail | None = None,
        event_emitter: EventEmitter | None = None,
    ) -> None:
        self.llm = llm_client or MockLLMClient()
        self.policy = policy_engine or PolicyEngine()
        self.executor = tool_executor or ToolExecutor()
        self.audit = audit_trail or AuditTrail()
        self.events = event_emitter or EventEmitter()

    async def process_message(
        self, session: AgentSession, borrower_message: str
    ) -> ConversationTurn:
        state_before = session.state.value

        confirmation = detect_confirmation(borrower_message)
        borrower_confirmed = confirmation is True

        segment_template = SegmentRegistry.get(session.segment or "")
        available_tools = ToolRegistry.get_available_for_state(session.state)
        tool_names = [t.name for t in available_tools]

        system_prompt = build_system_prompt(
            lender_name=session.lender_id,
            segment=segment_template,
            session_state=session.state,
            language=session.language,
            available_tools=tool_names,
        )

        messages = [LLMMessage(role="system", content=system_prompt)]
        messages.extend(session.messages)
        messages.append(LLMMessage(role="user", content=borrower_message))

        llm_response = await self.llm.chat(
            messages=messages,
            tools=[{"name": t.name, "description": t.description} for t in available_tools],
        )

        tools_called: list[str] = []
        tool_results: list[dict[str, Any]] = []

        if llm_response.tool_calls:
            for tc in llm_response.tool_calls:
                result = await self._execute_tool(
                    session, tc, borrower_confirmed
                )
                tools_called.append(tc.tool_name)
                tool_results.append({
                    "tool": tc.tool_name,
                    "status": result.status.value,
                    "data": result.data,
                })

                if (
                    result.status == ToolResultStatus.SUCCESS
                    and tc.tool_name in ("verify_aadhaar_otp", "verify_aadhaar_voice_otp")
                    and result.data
                    and result.data.get("verified")
                ):
                    session.state = SessionMachine.transition(
                        session.state, SessionState.VERIFIED
                    )
                    self.audit.log_state_transition(
                        session.session_id,
                        state_before,
                        session.state.value,
                        tc.tool_name,
                        session.lender_id,
                    )

                self.audit.log_tool_execution(
                    session_id=session.session_id,
                    tool_name=tc.tool_name,
                    tool_category=ToolRegistry.get(tc.tool_name).category.value
                    if ToolRegistry.get(tc.tool_name)
                    else "unknown",
                    input_data=tc.arguments,
                    output_data=result.data,
                    result_status=result.status.value,
                    session_state_before=state_before,
                    session_state_after=session.state.value,
                    latency_ms=result.latency_ms,
                    lender_id=session.lender_id,
                    loan_application_id=session.loan_application_id,
                )

            if tool_results:
                result_prompt = build_tool_result_prompt(
                    tools_called[-1],
                    tool_results[-1].get("data", {}),
                    session.language,
                )
                messages.append(LLMMessage(role="system", content=result_prompt))
                llm_response = await self.llm.chat(messages=messages)

        agent_response = llm_response.content or "Main samajh gaya."

        behavioral_ctx = BehavioralContext(
            session_state=session.state,
            agent_response=agent_response,
            borrower_message=borrower_message,
            language=session.language,
            segment=session.segment or "",
            loan_terms_finalized=session.kfs_generated,
        )
        policy_result = self.policy.evaluate_response(behavioral_ctx)

        if not policy_result.allowed:
            agent_response = self._sanitize_response(
                agent_response, policy_result.blocking_rule or ""
            )

        turn = ConversationTurn(
            borrower_message=borrower_message,
            agent_response=agent_response,
            tools_called=tools_called,
            tool_results=tool_results,
            state_before=state_before,
            state_after=session.state.value,
        )
        session.history.append(turn)

        self.audit.log_event(
            session_id=session.session_id,
            event_type="CONVERSATION_TURN",
            event_data={
                "borrower_message_length": len(borrower_message),
                "tools_called": tools_called,
                "state_before": state_before,
                "state_after": session.state.value,
                "policy_warnings": policy_result.warnings,
            },
            lender_id=session.lender_id,
        )

        return turn

    async def _execute_tool(
        self,
        session: AgentSession,
        tool_call: ToolCall,
        borrower_confirmed: bool,
    ) -> ToolResult:
        ctx = ExecutionContext(
            session_id=session.session_id,
            session_state=session.state,
            lender_id=session.lender_id,
            loan_application_id=session.loan_application_id,
            borrower_confirmed=borrower_confirmed,
            maker_approved=session.maker_approved,
            kfs_generated=session.kfs_generated,
        )
        return await self.executor.execute(
            tool_call.tool_name, ctx, **tool_call.arguments
        )

    def _sanitize_response(self, response: str, blocking_rule: str) -> str:
        if blocking_rule == "rbi_fair_practices_language":
            return (
                "Main aapki baat samajhta hoon. "
                "Kya main aapki kisi aur tarah se madad kar sakta hoon?"
            )
        if blocking_rule == "pii_masked_readback":
            return (
                "Aapki jaankari surakshit hai. "
                "Main sirf antim 4 digit bata sakta hoon."
            )
        if blocking_rule == "no_disclosure_before_verify":
            return (
                "Pehle aapki pehchaan verify karni hogi. "
                "Kya aap apna Aadhaar number bata sakte hain?"
            )
        if blocking_rule == "grievance_disclosure":
            return (
                "Main aapki pareshani samajhta hoon. "
                "Aap hamare grievance officer se sampark kar sakte hain."
            )
        return response
