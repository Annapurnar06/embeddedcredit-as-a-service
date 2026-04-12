from app.models.session import SessionState
from app.policy.behavioral import BehavioralContext
from app.policy.engine import PolicyEngine
from app.policy.structural import PolicyContext
from app.tools.registry import AuthorityLevel, ToolCategory, ToolDefinition


def _tool(
    name: str = "test_tool",
    category: ToolCategory = ToolCategory.DATA,
    requires_confirmation: bool = False,
    authority_level: AuthorityLevel = AuthorityLevel.GENERAL,
) -> ToolDefinition:
    async def noop(**kwargs):
        return {}

    return ToolDefinition(
        name=name,
        description="test",
        category=category,
        handler=noop,
        requires_confirmation=requires_confirmation,
        authority_level=authority_level,
    )


engine = PolicyEngine()


class TestToolCallEvaluation:
    def test_allows_valid_call(self):
        result = engine.evaluate_tool_call(
            _tool(category=ToolCategory.DATA),
            PolicyContext(session_state=SessionState.VERIFIED),
        )
        assert result.allowed is True
        assert result.blocking_rule is None

    def test_blocks_invalid_state(self):
        result = engine.evaluate_tool_call(
            _tool(category=ToolCategory.DATA),
            PolicyContext(session_state=SessionState.UNVERIFIED),
        )
        assert result.allowed is False
        assert result.blocking_rule == "identity_gate"

    def test_blocks_missing_confirmation(self):
        result = engine.evaluate_tool_call(
            _tool(requires_confirmation=True),
            PolicyContext(
                session_state=SessionState.VERIFIED,
                borrower_confirmed=False,
            ),
        )
        assert result.allowed is False
        assert result.blocking_rule == "write_confirmation"

    def test_result_to_dict(self):
        result = engine.evaluate_tool_call(
            _tool(category=ToolCategory.DATA),
            PolicyContext(session_state=SessionState.VERIFIED),
        )
        d = result.to_dict()
        assert d["allowed"] is True
        assert len(d["structural_checks"]) == 7


class TestResponseEvaluation:
    def test_allows_clean_response(self):
        result = engine.evaluate_response(
            BehavioralContext(
                session_state=SessionState.VERIFIED,
                agent_response="Namaste, how can I help?",
            )
        )
        assert result.allowed is True

    def test_blocks_coercive_response(self):
        result = engine.evaluate_response(
            BehavioralContext(
                session_state=SessionState.VERIFIED,
                agent_response="We will take legal action against you",
            )
        )
        assert result.allowed is False
        assert result.blocking_rule == "rbi_fair_practices_language"

    def test_blocks_pii_leak(self):
        result = engine.evaluate_response(
            BehavioralContext(
                session_state=SessionState.VERIFIED,
                agent_response="Your Aadhaar is 1234 5678 9012",
            )
        )
        assert result.allowed is False
        assert result.blocking_rule == "pii_masked_readback"

    def test_captures_warnings(self):
        result = engine.evaluate_response(
            BehavioralContext(
                session_state=SessionState.VERIFIED,
                agent_response="Aapko milega 2 lakh guaranteed",
                loan_terms_finalized=False,
            )
        )
        assert len(result.warnings) > 0

    def test_result_has_behavioral_checks(self):
        result = engine.evaluate_response(
            BehavioralContext(
                session_state=SessionState.VERIFIED,
                agent_response="Hello",
            )
        )
        d = result.to_dict()
        assert len(d["behavioral_checks"]) == 10
