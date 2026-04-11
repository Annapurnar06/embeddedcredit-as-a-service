"""What-if simulation for policy parameter changes."""
from __future__ import annotations

from app.schemas.loan import WhatIfResult
from app.tools.registry import AuthorityLevel, ToolCategory, lending_tool


@lending_tool(
    name="run_what_if",
    description="Simulate policy parameter changes and project impact",
    category=ToolCategory.SCORING,
    authority_level=AuthorityLevel.ACCOUNT,
    timeout_seconds=10,
)
async def run_what_if(
    parameter_changes: dict | None = None,
    current_approval_rate: float = 0.35,
    current_npa_rate: float = 0.05,
    portfolio_size: int = 1000,
) -> dict:
    changes = parameter_changes or {}
    approval_delta = 0.0
    npa_delta = 0.0

    if "min_score" in changes:
        score_change = int(changes["min_score"]) - 500
        approval_delta -= score_change * 0.001
        npa_delta -= score_change * 0.0005

    if "max_amount" in changes:
        npa_delta += 0.005

    return WhatIfResult(
        parameter_changes={k: str(v) for k, v in changes.items()},
        projected_approval_rate=round(current_approval_rate + approval_delta, 3),
        projected_npa_rate=round(current_npa_rate + npa_delta, 3),
        projected_portfolio_size=int(portfolio_size * (1 + approval_delta)),
        comparison_with_current={
            "approval_rate_change": f"{approval_delta:+.1%}",
            "npa_rate_change": f"{npa_delta:+.1%}",
        },
    ).model_dump()
