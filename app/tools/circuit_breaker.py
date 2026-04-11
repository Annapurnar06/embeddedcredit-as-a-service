from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


@dataclass
class CircuitBreaker:
    threshold: int = 5
    recovery_seconds: float = 30.0

    _failure_count: int = 0
    _state: CircuitState = CircuitState.CLOSED
    _last_failure_time: float = 0.0

    def is_open(self) -> bool:
        if self._state == CircuitState.OPEN:
            if time.monotonic() - self._last_failure_time >= self.recovery_seconds:
                self._state = CircuitState.HALF_OPEN
                return False
            return True
        return False

    def record_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.monotonic()
        if self._failure_count >= self.threshold:
            self._state = CircuitState.OPEN

    @property
    def state(self) -> CircuitState:
        if (
            self._state == CircuitState.OPEN
            and time.monotonic() - self._last_failure_time >= self.recovery_seconds
        ):
            return CircuitState.HALF_OPEN
        return self._state

    @property
    def failure_count(self) -> int:
        return self._failure_count


class CircuitBreakerManager:
    _breakers: dict[str, CircuitBreaker] = {}

    @classmethod
    def get_or_create(cls, tool_name: str, threshold: int = 5) -> CircuitBreaker:
        if tool_name not in cls._breakers:
            cls._breakers[tool_name] = CircuitBreaker(threshold=threshold)
        return cls._breakers[tool_name]

    @classmethod
    def get(cls, tool_name: str) -> CircuitBreaker | None:
        return cls._breakers.get(tool_name)

    @classmethod
    def clear(cls) -> None:
        cls._breakers.clear()
