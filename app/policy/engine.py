"""Policy engine -- orchestrates structural + behavioral rule evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.policy.behavioral import (
    BehavioralCheckResult,
    BehavioralContext,
    evaluate_behavioral_policies,
    get_violations,
    has_errors,
)
from app.policy.structural import (
    PolicyCheckResult,
    PolicyContext,
    any_blocked,
    evaluate_structural_policies,
)
from app.tools.registry import ToolDefinition


@dataclass
class PolicyEvaluationResult:
    allowed: bool
    structural_results: list[PolicyCheckResult] = field(default_factory=list)
    behavioral_results: list[BehavioralCheckResult] = field(default_factory=list)
    blocking_rule: str | None = None
    blocking_reason: str | None = None
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed": self.allowed,
            "blocking_rule": self.blocking_rule,
            "blocking_reason": self.blocking_reason,
            "warnings": self.warnings,
            "structural_checks": [
                {"rule": r.rule_name, "passed": r.passed, "reason": r.reason}
                for r in self.structural_results
            ],
            "behavioral_checks": [
                {
                    "rule": r.rule_name,
                    "passed": r.passed,
                    "severity": r.severity,
                    "reason": r.reason,
                }
                for r in self.behavioral_results
            ],
        }


class PolicyEngine:
    def evaluate_tool_call(
        self,
        tool: ToolDefinition,
        ctx: PolicyContext,
    ) -> PolicyEvaluationResult:
        structural = evaluate_structural_policies(tool, ctx)
        blocked = any_blocked(structural)
        if blocked:
            return PolicyEvaluationResult(
                allowed=False,
                structural_results=structural,
                blocking_rule=blocked.rule_name,
                blocking_reason=blocked.reason,
            )
        return PolicyEvaluationResult(
            allowed=True,
            structural_results=structural,
        )

    def evaluate_response(
        self,
        ctx: BehavioralContext,
    ) -> PolicyEvaluationResult:
        behavioral = evaluate_behavioral_policies(ctx)
        violations = get_violations(behavioral)
        warnings = [v.reason for v in violations if v.severity == "warning"]
        blocked = has_errors(behavioral)

        if blocked:
            error = next(v for v in violations if v.severity == "error")
            return PolicyEvaluationResult(
                allowed=False,
                behavioral_results=behavioral,
                blocking_rule=error.rule_name,
                blocking_reason=error.reason,
                warnings=warnings,
            )
        return PolicyEvaluationResult(
            allowed=True,
            behavioral_results=behavioral,
            warnings=warnings,
        )
