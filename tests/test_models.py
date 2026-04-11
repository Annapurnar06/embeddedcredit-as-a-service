from app.models.loan import LoanStatus
from app.models.session import SessionState


def test_session_states():
    assert SessionState.UNVERIFIED.value == "UNVERIFIED"
    assert SessionState.VERIFIED.value == "VERIFIED"
    assert SessionState.CONFIRMED.value == "CONFIRMED"
    assert SessionState.EXPIRED.value == "EXPIRED"


def test_loan_statuses():
    assert LoanStatus.DRAFT.value == "DRAFT"
    assert LoanStatus.DISBURSED.value == "DISBURSED"
    assert LoanStatus.ACTIVE.value == "ACTIVE"
    assert LoanStatus.NPA.value == "NPA"
    all_statuses = [s.value for s in LoanStatus]
    assert len(all_statuses) == 15


def test_session_state_ordering():
    states = [SessionState.UNVERIFIED, SessionState.VERIFIED, SessionState.CONFIRMED]
    assert states[0] == SessionState.UNVERIFIED
    assert states[1] == SessionState.VERIFIED
    assert states[2] == SessionState.CONFIRMED
