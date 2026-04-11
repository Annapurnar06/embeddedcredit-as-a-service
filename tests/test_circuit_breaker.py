import time

from app.tools.circuit_breaker import CircuitBreaker, CircuitBreakerManager, CircuitState


def test_initial_state():
    cb = CircuitBreaker(threshold=3)
    assert cb.state == CircuitState.CLOSED
    assert cb.failure_count == 0
    assert not cb.is_open()


def test_records_success():
    cb = CircuitBreaker(threshold=3)
    cb.record_failure()
    cb.record_failure()
    assert cb.failure_count == 2
    cb.record_success()
    assert cb.failure_count == 0
    assert cb.state == CircuitState.CLOSED


def test_opens_after_threshold():
    cb = CircuitBreaker(threshold=3)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.CLOSED
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    assert cb.is_open()


def test_half_open_after_recovery():
    cb = CircuitBreaker(threshold=2, recovery_seconds=0.1)
    cb.record_failure()
    cb.record_failure()
    assert cb.state == CircuitState.OPEN
    time.sleep(0.15)
    assert cb.state == CircuitState.HALF_OPEN
    assert not cb.is_open()


def test_manager_get_or_create():
    CircuitBreakerManager.clear()
    cb1 = CircuitBreakerManager.get_or_create("tool_a", threshold=3)
    cb2 = CircuitBreakerManager.get_or_create("tool_a", threshold=5)
    assert cb1 is cb2
    assert cb1.threshold == 3

    cb3 = CircuitBreakerManager.get_or_create("tool_b", threshold=5)
    assert cb3 is not cb1
    assert cb3.threshold == 5
    CircuitBreakerManager.clear()
