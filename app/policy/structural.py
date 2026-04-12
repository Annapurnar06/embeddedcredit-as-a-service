"""7 structural policy rules -- deterministic, no LLM, run BEFORE every tool call."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.core.config import settings
from app.models.session import SessionState
from app.tools.registry import AuthorityLevel, ToolCategory, ToolDefinition


@dataclass
class PolicyCheckResult:
    rule_name: str
    passed: bool
    reason: str = ""
    metadata: dict[str, Any] | None = None


@dataclass
class PolicyContext:
    session_state: SessionState
    borrower_confirmed: bool = False
    maker_approved: bool = False
    kfs_generated: bool = False
    bureau_pulls_48h: int = 0
    consent_tokens: dict[str, bool] | None = None
    cooling_off_end: str | None = None
    current_timestamp: str | None = None


def check_identity_gate(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block account-detail disclosure when session_state == UNVERIFIED."""
    if ctx.session_state == SessionState.UNVERIFIED and tool.category not in (
        ToolCategory.IDENTITY,
    ):
        return PolicyCheckResult(
            rule_name="identity_gate",
            passed=False,
            reason=(
                f"Tool '{tool.name}' ({tool.category.value}) blocked: "
                f"session is UNVERIFIED. Only identity tools allowed."
            ),
        )
    return PolicyCheckResult(rule_name="identity_gate", passed=True)


def check_write_confirmation(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block write tools without explicit borrower confirmation."""
    if tool.requires_confirmation and not ctx.borrower_confirmed:
        return PolicyCheckResult(
            rule_name="write_confirmation",
            passed=False,
            reason=(
                f"Tool '{tool.name}' requires explicit borrower confirmation "
                f"(haan/theek hai/yes/confirm). None detected."
            ),
        )
    return PolicyCheckResult(rule_name="write_confirmation", passed=True)


def check_kfs_mandatory(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block disbursement without KFS generation (RBI Digital Lending Direction)."""
    if tool.name in ("execute_disbursement", "initiate_esign") and not ctx.kfs_generated:
        return PolicyCheckResult(
            rule_name="kfs_mandatory",
            passed=False,
            reason=(
                f"Tool '{tool.name}' blocked: Key Fact Statement not yet generated. "
                f"RBI Digital Lending Directions require KFS before disbursement."
            ),
        )
    return PolicyCheckResult(rule_name="kfs_mandatory", passed=True)


def check_bureau_velocity(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block bureau pull if >N pulls for same Aadhaar in 48h."""
    if tool.name == "pull_credit_bureau":
        max_pulls = settings.bureau_pull_max_per_aadhaar_48h
        if ctx.bureau_pulls_48h >= max_pulls:
            return PolicyCheckResult(
                rule_name="bureau_velocity",
                passed=False,
                reason=(
                    f"Bureau pull blocked: {ctx.bureau_pulls_48h} pulls in last 48h "
                    f"(max: {max_pulls}). Protects borrower credit score."
                ),
                metadata={"pulls_48h": ctx.bureau_pulls_48h, "max": max_pulls},
            )
    return PolicyCheckResult(rule_name="bureau_velocity", passed=True)


def check_cooling_off_period(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block disbursement within cooling-off period (RBI mandate)."""
    if (
        tool.name == "execute_disbursement"
        and ctx.cooling_off_end
        and ctx.current_timestamp
        and ctx.current_timestamp < ctx.cooling_off_end
    ):
        return PolicyCheckResult(
            rule_name="cooling_off_period",
            passed=False,
            reason=(
                f"Disbursement blocked: cooling-off period active until "
                f"{ctx.cooling_off_end}. RBI product-specific mandate."
            ),
        )
    return PolicyCheckResult(rule_name="cooling_off_period", passed=True)


def check_consent_required(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block ULI/AA data fetch without valid consent token."""
    consent_tools = {
        "fetch_aa_bank_data",
        "fetch_uli_parallel",
        "fetch_cooperative_data",
        "fetch_platform_earnings",
        "fetch_gst_returns",
    }
    if tool.name in consent_tools:
        tokens = ctx.consent_tokens or {}
        if not tokens.get(tool.name, False):
            return PolicyCheckResult(
                rule_name="consent_required",
                passed=False,
                reason=(
                    f"Tool '{tool.name}' blocked: valid consent token not found. "
                    f"Data fetch requires borrower consent."
                ),
            )
    return PolicyCheckResult(rule_name="consent_required", passed=True)


def check_maker_checker(tool: ToolDefinition, ctx: PolicyContext) -> PolicyCheckResult:
    """Block disbursement without human approval flag (Phase 1: 100% human review)."""
    if (
        tool.authority_level == AuthorityLevel.WRITE
        and not ctx.maker_approved
        and not settings.can_disburse_without_human
    ):
        return PolicyCheckResult(
            rule_name="maker_checker",
            passed=False,
            reason=(
                f"Tool '{tool.name}' blocked: maker-checker approval required. "
                f"Phase 1: all write operations need human approval."
            ),
        )
    return PolicyCheckResult(rule_name="maker_checker", passed=True)


STRUCTURAL_RULES = [
    check_identity_gate,
    check_write_confirmation,
    check_kfs_mandatory,
    check_bureau_velocity,
    check_cooling_off_period,
    check_consent_required,
    check_maker_checker,
]


def evaluate_structural_policies(
    tool: ToolDefinition, ctx: PolicyContext
) -> list[PolicyCheckResult]:
    results = []
    for rule_fn in STRUCTURAL_RULES:
        result = rule_fn(tool, ctx)
        results.append(result)
    return results


def any_blocked(results: list[PolicyCheckResult]) -> PolicyCheckResult | None:
    for r in results:
        if not r.passed:
            return r
    return None
