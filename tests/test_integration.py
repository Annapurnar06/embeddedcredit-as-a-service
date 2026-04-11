"""End-to-end integration tests -- full loan lifecycle flows."""
import uuid

import pytest
from httpx import ASGITransport, AsyncClient

from app.agent.runtime import AgentRuntime, AgentSession
from app.core.audit import AuditTrail
from app.main import app
from app.models.session import SessionState
from app.tools.circuit_breaker import CircuitBreakerManager
from app.tools.data import *  # noqa: F401,F403
from app.tools.execution import *  # noqa: F401,F403
from app.tools.executor import ExecutionContext, ToolExecutor
from app.tools.identity import *  # noqa: F401,F403
from app.tools.monitoring import *  # noqa: F401,F403
from app.tools.product import *  # noqa: F401,F403
from app.tools.registry import ToolRegistry, ToolResultStatus
from app.tools.scoring import *  # noqa: F401,F403
from app.tools.servicing import *  # noqa: F401,F403


@pytest.fixture(autouse=True)
def setup():
    CircuitBreakerManager.clear()
    yield


class TestDairyFarmerOrigination:
    """Full dairy farmer origination: identity -> data -> score -> product -> execute."""

    @pytest.mark.asyncio
    async def test_full_flow(self):
        ex = ToolExecutor()
        sid = uuid.uuid4()

        # Phase 1: Identity Verification (UNVERIFIED state)
        ctx = ExecutionContext(
            session_id=sid,
            session_state=SessionState.UNVERIFIED,
            lender_id="NBFC_001",
        )
        r = await ex.execute(
            "verify_aadhaar_otp", ctx,
            aadhaar_number="123456789012", otp="123456",
        )
        assert r.status == ToolResultStatus.SUCCESS
        assert r.data["verified"] is True

        r = await ex.execute(
            "verify_pan", ctx,
            pan_number="ABCDE1234F", aadhaar_name="Ramesh Patel",
        )
        assert r.status == ToolResultStatus.SUCCESS

        # Phase 2: Data Assembly (VERIFIED state)
        ctx = ExecutionContext(
            session_id=sid,
            session_state=SessionState.VERIFIED,
            lender_id="NBFC_001",
            borrower_confirmed=True,
        )
        r = await ex.execute("fetch_uli_parallel", ctx)
        assert r.status == ToolResultStatus.SUCCESS

        r = await ex.execute("fetch_aa_bank_data", ctx)
        assert r.status == ToolResultStatus.SUCCESS

        r = await ex.execute(
            "pull_credit_bureau", ctx,
            bureau="CIBIL", aadhaar_hash="abc123",
        )
        assert r.status == ToolResultStatus.SUCCESS

        r = await ex.execute("analyze_bank_statement", ctx)
        assert r.status == ToolResultStatus.SUCCESS

        r = await ex.execute("compute_borrower_profile", ctx)
        assert r.status == ToolResultStatus.SUCCESS

        # Phase 3: Scoring (VERIFIED state)
        r = await ex.execute(
            "evaluate_segment_policy", ctx,
            segment="DAIRY_FARMER", score=700,
            confidence_level="HIGH",
        )
        assert r.data["decision"] == "APPROVE"

        r = await ex.execute(
            "compute_segment_score", ctx,
            segment="DAIRY_FARMER",
            features={
                "pouring_regularity": 0.92,
                "bureau_score": 720,
                "bank_stability": 0.85,
            },
        )
        assert r.data["score"] > 0

        r = await ex.execute("compute_risk_pricing", ctx, score=700)
        assert r.data["rate_band"] is not None

        r = await ex.execute(
            "check_fraud_signals", ctx, device_fingerprint="fp_123",
        )
        assert r.data["result"] == "PASS"

        # Phase 4: Product Design
        r = await ex.execute(
            "design_dynamic_product", ctx,
            segment="DAIRY_FARMER", score=700,
            requested_amount=100000,
        )
        assert r.data["schedule_type"] == "SEASONAL_DYNAMIC"

        r = await ex.execute(
            "generate_seasonal_schedule", ctx,
            amount=100000, rate=15.0, tenure_months=12,
        )
        assert len(r.data["entries"]) == 12

        # Phase 5: Execution (CONFIRMED state)
        ctx = ExecutionContext(
            session_id=sid,
            session_state=SessionState.CONFIRMED,
            lender_id="NBFC_001",
            borrower_confirmed=True,
            maker_approved=True,
            kfs_generated=True,
        )
        r = await ex.execute(
            "generate_kfs", ctx,
            borrower_name="Ramesh Patel", amount=100000,
            rate=15.0, tenure_months=12,
        )
        assert r.data["cooling_off_period_days"] == 3

        r = await ex.execute("initiate_esign", ctx)
        assert r.data["status"] == "OTP_SENT"

        r = await ex.execute(
            "enroll_insurance", ctx,
            insurance_type="PASHU_BIMA", sum_insured=80000,
        )
        assert r.data["status"] == "ENROLLED"

        r = await ex.execute(
            "setup_enach_mandate", ctx, max_amount=8000,
        )
        assert r.data["mode"] == "eNACH"

        r = await ex.execute(
            "execute_disbursement", ctx,
            amount=100000, mode="UPI",
        )
        assert r.data["status"] == "SUCCESS"

        r = await ex.execute(
            "register_cersai", ctx,
            asset_type="LIVESTOCK",
            asset_description="5 milch cows",
        )
        assert r.data["status"] == "REGISTERED"


class TestReferFlow:
    """Test REFER decision -- partial approval with human review."""

    @pytest.mark.asyncio
    async def test_refer_decision(self):
        ex = ToolExecutor()
        ctx = ExecutionContext(
            session_id=uuid.uuid4(),
            session_state=SessionState.VERIFIED,
            lender_id="NBFC_001",
        )
        r = await ex.execute(
            "evaluate_segment_policy", ctx,
            segment="DAIRY_FARMER", score=550,
            confidence_level="LOW",
        )
        assert r.data["decision"] == "REFER"

        r = await ex.execute(
            "generate_cam", ctx,
            borrower_name="Suresh Kumar",
            segment="DAIRY_FARMER",
            score=550, score_grade="B2",
            income_monthly=25000,
        )
        assert "Suresh" in r.data["borrower_summary"]

        r = await ex.execute(
            "generate_explainability", ctx,
            decision="REFER",
            reason_codes=["SCORE_BELOW_MINIMUM"],
            language="hi",
        )
        assert len(r.data["borrower_facing_reasons"]) > 0


class TestMonitoringFlow:
    """Test post-disbursement monitoring pipeline."""

    @pytest.mark.asyncio
    async def test_monitoring_pipeline(self):
        ex = ToolExecutor()
        ctx = ExecutionContext(
            session_id=uuid.uuid4(),
            session_state=SessionState.VERIFIED,
            lender_id="NBFC_001",
        )

        r = await ex.execute("poll_monitoring_signals", ctx)
        assert r.data["signals_polled"] > 0

        signals = [
            {"signal_type": "bank_txn_drop", "value": 0.8},
            {"signal_type": "cooperative_pouring_drop", "value": 0.9},
        ]
        r = await ex.execute(
            "evaluate_monitoring_triggers", ctx,
            segment="DAIRY_FARMER", signals=signals,
        )
        assert r.data["recommended_action"] in ("WATCH", "ESCALATE")

        r = await ex.execute(
            "evaluate_graduation", ctx,
            months_on_book=12, on_time_rate=0.98,
        )
        assert r.data["eligible"] is True


class TestServicingFlow:
    """Test post-disbursement servicing."""

    @pytest.mark.asyncio
    async def test_servicing_pipeline(self):
        ex = ToolExecutor()
        ctx = ExecutionContext(
            session_id=uuid.uuid4(),
            session_state=SessionState.VERIFIED,
            lender_id="NBFC_001",
            borrower_confirmed=True,
            maker_approved=True,
        )

        r = await ex.execute("get_loan_status", ctx)
        assert r.data["status"] == "ACTIVE"

        r = await ex.execute("get_repayment_schedule", ctx)
        assert len(r.data["entries"]) == 18

        r = await ex.execute(
            "process_prepayment", ctx,
            amount=10000, mode="reduce_tenure",
        )
        assert r.data["months_saved"] == 2

        r = await ex.execute("generate_statement", ctx)
        assert r.data["generated"] is True


class TestAgentConversationFlow:
    """Test multi-turn agent conversation."""

    @pytest.mark.asyncio
    async def test_dairy_farmer_conversation(self):
        audit = AuditTrail()
        runtime = AgentRuntime(audit_trail=audit)
        session = AgentSession(
            session_id=uuid.uuid4(),
            lender_id="TEST_NBFC",
            state=SessionState.UNVERIFIED,
            segment="DAIRY_FARMER",
            language="hi",
        )

        t1 = await runtime.process_message(session, "namaste")
        assert t1.agent_response != ""
        assert t1.state_after == "UNVERIFIED"

        t2 = await runtime.process_message(session, "mujhe loan chahiye")
        assert t2.agent_response != ""

        await runtime.process_message(
            session, "verify my aadhaar 123456789012"
        )
        assert len(session.history) == 3

        assert audit.total_logs >= 3


class TestAPIEndpoints:
    """Test all API endpoints."""

    @pytest.mark.asyncio
    async def test_health(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            resp = await client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_chat_flow(self):
        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as client:
            r1 = await client.post(
                "/api/chat/message",
                json={
                    "channel": "web",
                    "channel_user_id": "integ_user_1",
                    "lender_id": "TEST_NBFC",
                    "content": "namaste",
                    "segment": "DAIRY_FARMER",
                },
            )
            assert r1.status_code == 200
            data1 = r1.json()
            assert data1["state"] == "UNVERIFIED"

            r2 = await client.post(
                "/api/chat/message",
                json={
                    "channel": "web",
                    "channel_user_id": "integ_user_1",
                    "lender_id": "TEST_NBFC",
                    "content": "verify my aadhaar please",
                },
            )
            assert r2.status_code == 200


class TestToolCoverage:
    """Verify all 48 tools are registered and reachable."""

    def test_total_tool_count(self):
        all_tools = list(ToolRegistry.get_all().values())
        assert len(all_tools) >= 48, (
            f"Expected >= 48 tools, got {len(all_tools)}: "
            f"{[t.name for t in all_tools]}"
        )

    def test_identity_tools(self):
        names = [
            "verify_aadhaar_otp", "verify_aadhaar_voice_otp",
            "verify_pan", "verify_bank_account",
            "initiate_aa_consent", "check_negative_list",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_data_tools(self):
        names = [
            "fetch_uli_parallel", "fetch_aa_bank_data",
            "pull_credit_bureau", "analyze_bank_statement",
            "extract_document", "fetch_cooperative_data",
            "fetch_platform_earnings", "fetch_gst_returns",
            "compute_device_score", "cross_validate_sources",
            "compute_confidence_score", "compute_borrower_profile",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_scoring_tools(self):
        names = [
            "evaluate_segment_policy", "compute_segment_score",
            "compute_risk_pricing", "check_fraud_signals",
            "generate_cam", "run_what_if",
            "check_psl_classification", "generate_explainability",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_product_tools(self):
        names = [
            "design_dynamic_product", "generate_seasonal_schedule",
            "generate_daily_micro_schedule",
            "generate_payout_linked_schedule",
            "compute_insurance_premium",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_execution_tools(self):
        names = [
            "generate_kfs", "initiate_esign", "enroll_insurance",
            "setup_enach_mandate", "execute_disbursement",
            "register_cersai",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_servicing_tools(self):
        names = [
            "get_loan_status", "get_repayment_schedule",
            "process_prepayment", "apply_moratorium",
            "generate_statement", "generate_noc",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"

    def test_monitoring_tools(self):
        names = [
            "poll_monitoring_signals",
            "evaluate_monitoring_triggers",
            "execute_auto_intervention",
            "evaluate_graduation",
            "schedule_monitoring_job",
        ]
        for n in names:
            assert ToolRegistry.get(n) is not None, f"Missing: {n}"
