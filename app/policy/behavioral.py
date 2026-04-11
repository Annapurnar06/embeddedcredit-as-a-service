"""10 behavioral supervisor rules -- evaluated per agent response turn.

These rules check the AGENT'S RESPONSE text for policy violations.
In production, these are LLM-evaluated. For now, we use regex/heuristic checks
that can be swapped for LLM calls later.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from app.models.session import SessionState


@dataclass
class BehavioralCheckResult:
    rule_name: str
    passed: bool
    severity: str = "warning"
    reason: str = ""
    suggested_fix: str = ""


@dataclass
class BehavioralContext:
    session_state: SessionState
    agent_response: str
    borrower_message: str = ""
    language: str = "hi"
    segment: str = ""
    loan_terms_finalized: bool = False


def check_no_disclosure_before_verify(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Never disclose loan-specific info before Aadhaar verification."""
    if ctx.session_state == SessionState.UNVERIFIED:
        loan_terms = re.compile(
            r"(loan amount|interest rate|emi|tenure|disburs|sanction|"
            r"rin rashi|byaj dar|kist|avadhi)",
            re.IGNORECASE,
        )
        if loan_terms.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="no_disclosure_before_verify",
                passed=False,
                severity="error",
                reason="Agent disclosed loan-specific information before identity verification.",
                suggested_fix="Remove loan details. Redirect to Aadhaar verification first.",
            )
    return BehavioralCheckResult(rule_name="no_disclosure_before_verify", passed=True)


def check_rbi_fair_practices_language(ctx: BehavioralContext) -> BehavioralCheckResult:
    """All communication must be non-coercive. No threatening language."""
    coercive = re.compile(
        r"(legal action|police|arrest|seize|garnish|threat|"
        r"kanuni karwahi|police|giraftaar|jabti)",
        re.IGNORECASE,
    )
    if coercive.search(ctx.agent_response):
        return BehavioralCheckResult(
            rule_name="rbi_fair_practices_language",
            passed=False,
            severity="error",
            reason="Agent used coercive/threatening language. RBI Fair Practices Code violation.",
            suggested_fix="Rephrase using empathetic, non-coercive language.",
        )
    return BehavioralCheckResult(rule_name="rbi_fair_practices_language", passed=True)


def check_no_commitment_on_terms(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Agent must not commit to specific loan terms until policy evaluation completes."""
    if not ctx.loan_terms_finalized:
        commitment = re.compile(
            r"(you will get|aapko milega|guaranteed|pakka|"
            r"definitely|zaroor milega|confirm amount)",
            re.IGNORECASE,
        )
        if commitment.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="no_commitment_on_terms",
                passed=False,
                severity="warning",
                reason="Agent committed to terms before policy evaluation.",
                suggested_fix="Use tentative language: 'subject to evaluation', 'may be eligible'.",
            )
    return BehavioralCheckResult(rule_name="no_commitment_on_terms", passed=True)


def check_psl_accurate_classification(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Never misrepresent loan purpose for PSL classification."""
    misrep = re.compile(
        r"(we.?ll classify|mark it as|show as agriculture|psl benefit)",
        re.IGNORECASE,
    )
    if misrep.search(ctx.agent_response):
        return BehavioralCheckResult(
            rule_name="psl_accurate_classification",
            passed=False,
            severity="error",
            reason="Agent suggested PSL misclassification.",
            suggested_fix=(
                "Remove PSL references. Classification is automatic based on purpose."
            ),
        )
    return BehavioralCheckResult(rule_name="psl_accurate_classification", passed=True)


def check_empathetic_tone_distress(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Use empathetic language when borrower describes hardship."""
    distress = re.compile(
        r"(death|died|flood|drought|accident|hospital|illness|"
        r"maut|bimari|baadh|sukha|durghatna)",
        re.IGNORECASE,
    )
    if distress.search(ctx.borrower_message):
        empathy = re.compile(
            r"(sorry|understand|difficult|help|support|"
            r"dukh|samajhte|mushkil|madad|sahayata)",
            re.IGNORECASE,
        )
        if not empathy.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="empathetic_tone_distress",
                passed=False,
                severity="warning",
                reason="Borrower expressed distress but agent response lacks empathy.",
                suggested_fix="Add empathetic acknowledgment before proceeding.",
            )
    return BehavioralCheckResult(rule_name="empathetic_tone_distress", passed=True)


def check_no_rate_guarantee(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Never guarantee a specific interest rate before formal approval."""
    if not ctx.loan_terms_finalized:
        guarantee = re.compile(
            r"(rate (will be|is)\s+\d|interest\s+\d+%|byaj\s+\d+)",
            re.IGNORECASE,
        )
        if guarantee.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="no_rate_guarantee",
                passed=False,
                severity="warning",
                reason="Agent guaranteed specific interest rate before approval.",
                suggested_fix="Use ranges: 'rates typically between X% and Y%'.",
            )
    return BehavioralCheckResult(rule_name="no_rate_guarantee", passed=True)


def check_insurance_opt_in(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Insurance must be presented as optional (except where policy-mandated)."""
    mandatory_ins = re.compile(
        r"(insurance.*mandatory|bima.*zaroori|must.*take.*insurance)",
        re.IGNORECASE,
    )
    if mandatory_ins.search(ctx.agent_response) and ctx.segment not in ("DAIRY_FARMER",):
        return BehavioralCheckResult(
            rule_name="insurance_opt_in",
            passed=False,
            severity="warning",
            reason="Agent presented insurance as mandatory for non-mandated segment.",
            suggested_fix="Present insurance as optional with benefits explained.",
        )
    return BehavioralCheckResult(rule_name="insurance_opt_in", passed=True)


def check_grievance_disclosure(ctx: BehavioralContext) -> BehavioralCheckResult:
    """When borrower expresses complaint, must disclose grievance redressal mechanism."""
    complaint = re.compile(
        r"(complaint|wrong|cheat|fraud|overcharg|shikayat|galat|dhoka)",
        re.IGNORECASE,
    )
    if complaint.search(ctx.borrower_message):
        grievance = re.compile(
            r"(grievance|complaint number|nodal officer|ombudsman|shikayat adhikari)",
            re.IGNORECASE,
        )
        if not grievance.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="grievance_disclosure",
                passed=False,
                severity="error",
                reason="Borrower raised complaint but agent didn't disclose grievance mechanism.",
                suggested_fix="Include grievance officer contact and RBI ombudsman reference.",
            )
    return BehavioralCheckResult(rule_name="grievance_disclosure", passed=True)


def check_no_override_on_authority(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Reject 'my manager approved' or 'RBI told me' override attempts."""
    override_attempt = re.compile(
        r"(manager (said|approved|told)|rbi (told|said|approved)|"
        r"special permission|exception.*approved)",
        re.IGNORECASE,
    )
    if override_attempt.search(ctx.borrower_message):
        compliance = re.compile(
            r"(policy|cannot|standard process|verify|unable to override)",
            re.IGNORECASE,
        )
        if not compliance.search(ctx.agent_response):
            return BehavioralCheckResult(
                rule_name="no_override_on_authority",
                passed=False,
                severity="error",
                reason="Social engineering attempt detected but agent didn't enforce policy.",
                suggested_fix=(
                    "Respond: 'I must follow standard process. Cannot accept overrides.'"
                ),
            )
    return BehavioralCheckResult(rule_name="no_override_on_authority", passed=True)


def check_pii_masked_readback(ctx: BehavioralContext) -> BehavioralCheckResult:
    """Only last 4 digits of Aadhaar/PAN/account number on readback."""
    full_aadhaar = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
    full_pan = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")

    if full_aadhaar.search(ctx.agent_response):
        return BehavioralCheckResult(
            rule_name="pii_masked_readback",
            passed=False,
            severity="error",
            reason="Agent disclosed full Aadhaar number in response.",
            suggested_fix="Mask to XXXX-XXXX-1234 format.",
        )
    if full_pan.search(ctx.agent_response):
        return BehavioralCheckResult(
            rule_name="pii_masked_readback",
            passed=False,
            severity="error",
            reason="Agent disclosed full PAN number in response.",
            suggested_fix="Mask to XXXXX0000X format.",
        )
    return BehavioralCheckResult(rule_name="pii_masked_readback", passed=True)


BEHAVIORAL_RULES = [
    check_no_disclosure_before_verify,
    check_rbi_fair_practices_language,
    check_no_commitment_on_terms,
    check_psl_accurate_classification,
    check_empathetic_tone_distress,
    check_no_rate_guarantee,
    check_insurance_opt_in,
    check_grievance_disclosure,
    check_no_override_on_authority,
    check_pii_masked_readback,
]


def evaluate_behavioral_policies(
    ctx: BehavioralContext,
) -> list[BehavioralCheckResult]:
    return [rule_fn(ctx) for rule_fn in BEHAVIORAL_RULES]


def get_violations(
    results: list[BehavioralCheckResult],
) -> list[BehavioralCheckResult]:
    return [r for r in results if not r.passed]


def has_errors(results: list[BehavioralCheckResult]) -> bool:
    return any(r.severity == "error" and not r.passed for r in results)
