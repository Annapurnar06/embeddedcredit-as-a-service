"""mem0 memory integration -- persistent borrower memory across sessions.

Stores borrower context, preferences, conversation summaries, and interaction
patterns so the agent can recall prior interactions across channels and sessions.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@dataclass
class MemoryEntry:
    id: str
    user_id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""
    score: float = 1.0


@dataclass
class MemorySearchResult:
    memories: list[MemoryEntry] = field(default_factory=list)
    total: int = 0


class Mem0Client:
    """mem0 memory client -- stores and retrieves borrower context.

    When MEM0_API_KEY is set, uses the mem0 cloud API.
    Otherwise falls back to an in-memory store for development/testing.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or settings.mem0_api_key
        self._memory: dict[str, list[MemoryEntry]] | None = None
        self._client: Any = None

        if self.api_key:
            try:
                from mem0 import MemoryClient

                self._client = MemoryClient(api_key=self.api_key)
                logger.info("mem0_client_initialized", mode="cloud")
            except ImportError:
                logger.warning("mem0_package_not_installed", fallback="in_memory")
                self._memory = {}
        else:
            self._memory = {}
            logger.info("mem0_client_initialized", mode="in_memory")

    async def add(
        self,
        user_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> MemoryEntry:
        meta = metadata or {}
        meta["timestamp"] = datetime.now(timezone.utc).isoformat()

        if self._client:
            try:
                result = self._client.add(
                    messages=[{"role": "user", "content": content}],
                    user_id=user_id,
                    metadata=meta,
                )
                fallback_id = str(uuid.uuid4())
                mem_id = result.get("id", fallback_id) if isinstance(result, dict) else fallback_id
                return MemoryEntry(
                    id=mem_id,
                    user_id=user_id,
                    content=content,
                    metadata=meta,
                    created_at=meta["timestamp"],
                )
            except Exception as e:
                logger.error("mem0_add_error", error=str(e), user_id=user_id)

        entry = MemoryEntry(
            id=str(uuid.uuid4()),
            user_id=user_id,
            content=content,
            metadata=meta,
            created_at=meta["timestamp"],
            updated_at=meta["timestamp"],
        )
        if self._memory is not None:
            self._memory.setdefault(user_id, []).append(entry)
        return entry

    async def search(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
    ) -> MemorySearchResult:
        if self._client:
            try:
                results = self._client.search(query=query, user_id=user_id, limit=limit)
                memories = []
                for r in results if isinstance(results, list) else []:
                    memories.append(
                        MemoryEntry(
                            id=r.get("id", ""),
                            user_id=user_id,
                            content=r.get("memory", r.get("content", "")),
                            metadata=r.get("metadata", {}),
                            score=r.get("score", 1.0),
                        )
                    )
                return MemorySearchResult(memories=memories, total=len(memories))
            except Exception as e:
                logger.error("mem0_search_error", error=str(e), user_id=user_id)

        if self._memory is not None:
            entries = self._memory.get(user_id, [])
            query_lower = query.lower()
            matched = [e for e in entries if query_lower in e.content.lower()]
            if not matched:
                matched = entries[-limit:]
            return MemorySearchResult(memories=matched[:limit], total=len(matched))
        return MemorySearchResult()

    async def get_all(self, user_id: str) -> list[MemoryEntry]:
        if self._client:
            try:
                results = self._client.get_all(user_id=user_id)
                return [
                    MemoryEntry(
                        id=r.get("id", ""),
                        user_id=user_id,
                        content=r.get("memory", r.get("content", "")),
                        metadata=r.get("metadata", {}),
                    )
                    for r in (results if isinstance(results, list) else [])
                ]
            except Exception as e:
                logger.error("mem0_get_all_error", error=str(e), user_id=user_id)

        if self._memory is not None:
            return self._memory.get(user_id, [])
        return []

    async def delete(self, memory_id: str, user_id: str) -> bool:
        if self._client:
            try:
                self._client.delete(memory_id=memory_id)
                return True
            except Exception as e:
                logger.error("mem0_delete_error", error=str(e))
                return False

        if self._memory is not None:
            entries = self._memory.get(user_id, [])
            self._memory[user_id] = [e for e in entries if e.id != memory_id]
            return True
        return False

    async def delete_all(self, user_id: str) -> bool:
        if self._client:
            try:
                self._client.delete_all(user_id=user_id)
                return True
            except Exception as e:
                logger.error("mem0_delete_all_error", error=str(e))
                return False

        if self._memory is not None:
            self._memory.pop(user_id, None)
            return True
        return False


class BorrowerMemory:
    """High-level borrower memory manager built on mem0.

    Stores structured lending context: segment preferences, interaction history,
    repayment behavior, communication preferences, and prior application data.
    """

    def __init__(self, mem0: Mem0Client | None = None) -> None:
        self.mem0 = mem0 or Mem0Client()

    async def remember_interaction(
        self,
        borrower_id: str,
        session_id: str,
        summary: str,
        segment: str = "",
        tools_used: list[str] | None = None,
        outcome: str = "",
    ) -> MemoryEntry:
        content = f"Session {session_id}: {summary}"
        return await self.mem0.add(
            user_id=borrower_id,
            content=content,
            metadata={
                "type": "interaction",
                "session_id": session_id,
                "segment": segment,
                "tools_used": tools_used or [],
                "outcome": outcome,
            },
        )

    async def remember_preference(
        self,
        borrower_id: str,
        preference_key: str,
        preference_value: str,
    ) -> MemoryEntry:
        content = f"Preference: {preference_key} = {preference_value}"
        return await self.mem0.add(
            user_id=borrower_id,
            content=content,
            metadata={"type": "preference", "key": preference_key},
        )

    async def remember_application(
        self,
        borrower_id: str,
        loan_id: str,
        amount: float,
        product_type: str,
        status: str,
        segment: str = "",
    ) -> MemoryEntry:
        content = (
            f"Loan application {loan_id}: Rs {amount:,.0f} {product_type}, "
            f"status={status}, segment={segment}"
        )
        return await self.mem0.add(
            user_id=borrower_id,
            content=content,
            metadata={
                "type": "application",
                "loan_id": loan_id,
                "amount": amount,
                "product_type": product_type,
                "status": status,
                "segment": segment,
            },
        )

    async def remember_repayment_behavior(
        self,
        borrower_id: str,
        loan_id: str,
        behavior_summary: str,
    ) -> MemoryEntry:
        content = f"Repayment behavior for {loan_id}: {behavior_summary}"
        return await self.mem0.add(
            user_id=borrower_id,
            content=content,
            metadata={"type": "repayment_behavior", "loan_id": loan_id},
        )

    async def get_borrower_context(
        self,
        borrower_id: str,
        query: str = "",
    ) -> str:
        if query:
            result = await self.mem0.search(borrower_id, query, limit=5)
        else:
            entries = await self.mem0.get_all(borrower_id)
            result = MemorySearchResult(memories=entries[-10:], total=len(entries))

        if not result.memories:
            return ""

        context_parts = []
        for mem in result.memories:
            context_parts.append(mem.content)
        return "\n".join(context_parts)

    async def get_prior_applications(self, borrower_id: str) -> list[MemoryEntry]:
        entries = await self.mem0.get_all(borrower_id)
        return [e for e in entries if e.metadata.get("type") == "application"]

    async def get_communication_preference(self, borrower_id: str) -> dict[str, str]:
        entries = await self.mem0.get_all(borrower_id)
        prefs: dict[str, str] = {}
        for e in entries:
            if e.metadata.get("type") == "preference":
                prefs[e.metadata.get("key", "")] = e.content.split("=")[-1].strip()
        return prefs
