
from app.models.session import SessionState
from app.policy.structural import (
    PolicyContext,
    check_bureau_velocity,
    check_consent_required,
    check_identity_gate,
    check_kfs_mandatory,
    check_maker_checker,
    check_write_confirmation,
    evaluate_structural_policies,
)
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


def _ctx(**kwargs) -> PolicyContext:
    defaults = {"session_state": SessionState.VERIFIED}
    defaults.update(kwargs)
    return PolicyContext(**defaults)


class TestIdentityGate:
    def test_blocks_data_tool_in_unverified(self):
        result = check_identity_gate(
            _tool(category=ToolCategory.DATA),
            _ctx(session_state=SessionState.UNVERIFIED),
        )
        assert not result.passed
        assert "UNVERIFIED" in result.reason

    def test_allows_identity_tool_in_unverified(self):
        result = check_identity_gate(
            _tool(category=ToolCategory.IDENTITY),
            _ctx(session_state=SessionState.UNVERIFIED),
        )
        assert result.passed

    def test_allows_data_tool_in_verified(self):
        result = check_identity_gate(
            _tool(category=ToolCategory.DATA),
            _ctx(session_state=SessionState.VERIFIED),
        )
        assert result.passed


class TestWriteConfirmation:
    def test_blocks_without_confirmation(self):
        result = check_write_confirmation(
            _tool(requires_confirmation=True),
            _ctx(borrower_confirmed=False),
        )
        assert not result.passed

    def test_allows_with_confirmation(self):
        result = check_write_confirmation(
            _tool(requires_confirmation=True),
            _ctx(borrower_confirmed=True),
        )
        assert result.passed

    def test_allows_no_confirmation_needed(self):
        result = check_write_confirmation(
            _tool(requires_confirmation=False),
            _ctx(borrower_confirmed=False),
        )
        assert result.passed


class TestKfsMandatory:
    def test_blocks_disbursement_without_kfs(self):
        result = check_kfs_mandatory(
            _tool(name="execute_disbursement"),
            _ctx(kfs_generated=False),
        )
        assert not result.passed
        assert "Key Fact Statement" in result.reason

    def test_allows_disbursement_with_kfs(self):
        result = check_kfs_mandatory(
            _tool(name="execute_disbursement"),
            _ctx(kfs_generated=True),
        )
        assert result.passed

    def test_allows_other_tools_without_kfs(self):
        result = check_kfs_mandatory(
            _tool(name="compute_score"),
            _ctx(kfs_generated=False),
        )
        assert result.passed


class TestBureauVelocity:
    def test_blocks_at_max(self):
        result = check_bureau_velocity(
            _tool(name="pull_credit_bureau"),
            _ctx(bureau_pulls_48h=2),
        )
        assert not result.passed
        assert "48h" in result.reason

    def test_allows_below_max(self):
        result = check_bureau_velocity(
            _tool(name="pull_credit_bureau"),
            _ctx(bureau_pulls_48h=1),
        )
        assert result.passed

    def test_ignores_other_tools(self):
        result = check_bureau_velocity(
            _tool(name="verify_pan"),
            _ctx(bureau_pulls_48h=99),
        )
        assert result.passed


class TestConsentRequired:
    def test_blocks_aa_without_consent(self):
        result = check_consent_required(
            _tool(name="fetch_aa_bank_data"),
            _ctx(consent_tokens={}),
        )
        assert not result.passed
        assert "consent" in result.reason.lower()

    def test_allows_aa_with_consent(self):
        result = check_consent_required(
            _tool(name="fetch_aa_bank_data"),
            _ctx(consent_tokens={"fetch_aa_bank_data": True}),
        )
        assert result.passed

    def test_ignores_non_consent_tools(self):
        result = check_consent_required(
            _tool(name="verify_pan"),
            _ctx(consent_tokens={}),
        )
        assert result.passed


class TestMakerChecker:
    def test_blocks_write_without_approval(self):
        result = check_maker_checker(
            _tool(authority_level=AuthorityLevel.WRITE),
            _ctx(maker_approved=False),
        )
        assert not result.passed
        assert "maker-checker" in result.reason

    def test_allows_write_with_approval(self):
        result = check_maker_checker(
            _tool(authority_level=AuthorityLevel.WRITE),
            _ctx(maker_approved=True),
        )
        assert result.passed

    def test_allows_non_write(self):
        result = check_maker_checker(
            _tool(authority_level=AuthorityLevel.GENERAL),
            _ctx(maker_approved=False),
        )
        assert result.passed


class TestEvaluateAll:
    def test_all_7_rules_run(self):
        results = evaluate_structural_policies(
            _tool(), _ctx()
        )
        assert len(results) == 7

    def test_first_failure_captured(self):
        results = evaluate_structural_policies(
            _tool(category=ToolCategory.DATA),
            _ctx(session_state=SessionState.UNVERIFIED),
        )
        failed = [r for r in results if not r.passed]
        assert len(failed) >= 1
        assert failed[0].rule_name == "identity_gate"
