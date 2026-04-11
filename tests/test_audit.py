import uuid

from app.core.audit import AuditTrail, EventEmitter, mask_dict, mask_pii


class TestPiiMasking:
    def test_masks_aadhaar(self):
        assert mask_pii("Aadhaar: 1234 5678 9012") == "Aadhaar: XXXX-XXXX-XXXX"

    def test_masks_pan(self):
        assert mask_pii("PAN: ABCDE1234F") == "PAN: XXXXX0000X"

    def test_masks_phone(self):
        assert mask_pii("Phone: 9876543210") == "Phone: XXXXXXXXXX"

    def test_preserves_normal_text(self):
        assert mask_pii("Hello world") == "Hello world"

    def test_mask_dict_sensitive_keys(self):
        data = {"aadhaar_number": "123456789012", "name": "Ramesh"}
        masked = mask_dict(data)
        assert "1234" not in masked["aadhaar_number"]
        assert masked["name"] == "Ramesh"

    def test_mask_dict_nested(self):
        data = {"identity": {"pan_number": "ABCDE1234F"}}
        masked = mask_dict(data)
        assert masked["identity"]["pan_number"] == "XXXXX0000X"


class TestAuditTrail:
    def test_log_event(self):
        trail = AuditTrail()
        session_id = uuid.uuid4()
        entry = trail.log_event(
            session_id=session_id,
            event_type="KYC_VERIFIED",
            event_data={"aadhaar_hash": "abc123"},
            lender_id="LENDER_001",
        )
        assert entry["event_type"] == "KYC_VERIFIED"
        assert entry["session_id"] == str(session_id)
        assert trail.total_logs == 1

    def test_log_tool_execution(self):
        trail = AuditTrail()
        session_id = uuid.uuid4()
        entry = trail.log_tool_execution(
            session_id=session_id,
            tool_name="verify_aadhaar_otp",
            tool_category="identity",
            input_data={"aadhaar_number": "123456789012", "otp": "123456"},
            output_data={"verified": True},
            result_status="SUCCESS",
            session_state_before="UNVERIFIED",
            session_state_after="VERIFIED",
            latency_ms=150,
            lender_id="LENDER_001",
        )
        assert entry["tool_name"] == "verify_aadhaar_otp"
        assert "1234" not in entry["input_masked"]["aadhaar_number"]
        assert entry["input_masked"]["otp"] == "***MASKED***"  # int-like OTP masked entirely
        assert entry["output"] == {"verified": True}
        assert trail.total_tool_traces == 1

    def test_log_state_transition(self):
        trail = AuditTrail()
        session_id = uuid.uuid4()
        entry = trail.log_state_transition(
            session_id=session_id,
            from_state="UNVERIFIED",
            to_state="VERIFIED",
            trigger="verify_aadhaar_otp",
        )
        assert entry["event_type"] == "SESSION_STATE_TRANSITION"
        assert entry["event_data"]["from_state"] == "UNVERIFIED"

    def test_get_session_logs(self):
        trail = AuditTrail()
        s1 = uuid.uuid4()
        s2 = uuid.uuid4()
        trail.log_event(session_id=s1, event_type="E1", event_data={})
        trail.log_event(session_id=s2, event_type="E2", event_data={})
        trail.log_event(session_id=s1, event_type="E3", event_data={})
        assert len(trail.get_session_logs(s1)) == 2
        assert len(trail.get_session_logs(s2)) == 1

    def test_get_full_trail(self):
        trail = AuditTrail()
        session_id = uuid.uuid4()
        trail.log_event(session_id=session_id, event_type="START", event_data={})
        trail.log_tool_execution(
            session_id=session_id,
            tool_name="verify_aadhaar_otp",
            tool_category="identity",
            input_data={},
            output_data={},
            result_status="SUCCESS",
            session_state_before="UNVERIFIED",
            session_state_after="VERIFIED",
            latency_ms=100,
        )
        trail.log_event(session_id=session_id, event_type="END", event_data={})
        full = trail.get_full_trail(session_id)
        assert len(full) == 3
        types = [e["_type"] for e in full]
        assert "audit_log" in types
        assert "tool_execution" in types

    def test_failed_tool_no_output(self):
        trail = AuditTrail()
        entry = trail.log_tool_execution(
            session_id=uuid.uuid4(),
            tool_name="failing_tool",
            tool_category="data",
            input_data={},
            output_data=None,
            result_status="FAILURE",
            session_state_before="VERIFIED",
            session_state_after="VERIFIED",
            latency_ms=50,
            error_message="API timeout",
        )
        assert entry["output"] is None
        assert entry["error_message"] == "API timeout"


class TestEventEmitter:
    def test_emit_and_get(self):
        emitter = EventEmitter()
        emitter.emit("rl.signal", {"type": "KYC_VERIFIED", "loan_id": "L1"})
        emitter.emit("rl.signal", {"type": "SCORE_COMPUTED", "loan_id": "L1"})
        emitter.emit("monitor.heartbeat", {"loan_id": "L2"})
        assert emitter.total_events == 3
        assert len(emitter.get_events("rl.signal")) == 2
        assert len(emitter.get_events("monitor.heartbeat")) == 1
        assert len(emitter.get_events()) == 3
