"""Tests for mem0 memory integration -- borrower memory storage and retrieval."""

import pytest

from app.memory.mem0_client import BorrowerMemory, Mem0Client


class TestMem0Client:
    @pytest.fixture
    def client(self):
        return Mem0Client(api_key="")

    @pytest.mark.asyncio
    async def test_add_memory(self, client):
        entry = await client.add("borrower_001", "Applied for dairy loan")
        assert entry.id
        assert entry.user_id == "borrower_001"
        assert entry.content == "Applied for dairy loan"

    @pytest.mark.asyncio
    async def test_get_all(self, client):
        await client.add("b002", "First interaction")
        await client.add("b002", "Second interaction")
        entries = await client.get_all("b002")
        assert len(entries) == 2

    @pytest.mark.asyncio
    async def test_search(self, client):
        await client.add("b003", "Dairy farmer from Banaskantha")
        await client.add("b003", "Applied for seasonal loan")
        await client.add("b003", "Kirana shop query")
        result = await client.search("b003", "dairy")
        assert result.total >= 1
        assert any("dairy" in m.content.lower() for m in result.memories)

    @pytest.mark.asyncio
    async def test_search_empty(self, client):
        result = await client.search("nonexistent", "anything")
        assert result.total == 0

    @pytest.mark.asyncio
    async def test_delete(self, client):
        entry = await client.add("b004", "To delete")
        success = await client.delete(entry.id, "b004")
        assert success
        remaining = await client.get_all("b004")
        assert len(remaining) == 0

    @pytest.mark.asyncio
    async def test_delete_all(self, client):
        await client.add("b005", "Entry 1")
        await client.add("b005", "Entry 2")
        success = await client.delete_all("b005")
        assert success
        remaining = await client.get_all("b005")
        assert len(remaining) == 0

    @pytest.mark.asyncio
    async def test_add_with_metadata(self, client):
        meta = {"type": "inquiry", "segment": "GOLD_LOAN"}
        entry = await client.add("b006", "Gold loan inquiry", meta)
        assert entry.metadata["type"] == "inquiry"
        assert entry.metadata["segment"] == "GOLD_LOAN"


class TestBorrowerMemory:
    @pytest.fixture
    def memory(self):
        return BorrowerMemory(Mem0Client(api_key=""))

    @pytest.mark.asyncio
    async def test_remember_interaction(self, memory):
        entry = await memory.remember_interaction(
            borrower_id="bw_001",
            session_id="sess_abc",
            summary="Completed Aadhaar verification",
            segment="DAIRY_FARMER",
            tools_used=["verify_aadhaar_otp"],
            outcome="verified",
        )
        assert entry.id
        assert "sess_abc" in entry.content
        assert entry.metadata["type"] == "interaction"

    @pytest.mark.asyncio
    async def test_remember_application(self, memory):
        entry = await memory.remember_application(
            borrower_id="bw_002",
            loan_id="loan_xyz",
            amount=100000,
            product_type="seasonal_dynamic_emi",
            status="disbursed",
            segment="DAIRY_FARMER",
        )
        assert "100,000" in entry.content
        assert entry.metadata["type"] == "application"
        assert entry.metadata["loan_id"] == "loan_xyz"

    @pytest.mark.asyncio
    async def test_remember_preference(self, memory):
        entry = await memory.remember_preference("bw_003", "language", "gujarati")
        assert entry.metadata["type"] == "preference"
        assert entry.metadata["key"] == "language"

    @pytest.mark.asyncio
    async def test_get_borrower_context(self, memory):
        await memory.remember_interaction("bw_004", "s1", "First visit, asked about loan")
        await memory.remember_interaction("bw_004", "s2", "Completed KYC")
        ctx = await memory.get_borrower_context("bw_004")
        assert "First visit" in ctx
        assert "KYC" in ctx

    @pytest.mark.asyncio
    async def test_get_borrower_context_with_query(self, memory):
        await memory.remember_interaction("bw_005", "s1", "Dairy farmer from Gujarat")
        await memory.remember_interaction("bw_005", "s2", "Applied for kirana loan")
        ctx = await memory.get_borrower_context("bw_005", query="dairy")
        assert "dairy" in ctx.lower() or "Gujarat" in ctx

    @pytest.mark.asyncio
    async def test_get_prior_applications(self, memory):
        await memory.remember_application("bw_006", "l1", 50000, "micro", "disbursed")
        await memory.remember_interaction("bw_006", "s1", "General query")
        apps = await memory.get_prior_applications("bw_006")
        assert len(apps) == 1
        assert apps[0].metadata["type"] == "application"

    @pytest.mark.asyncio
    async def test_empty_context(self, memory):
        ctx = await memory.get_borrower_context("nonexistent")
        assert ctx == ""

    @pytest.mark.asyncio
    async def test_remember_repayment_behavior(self, memory):
        entry = await memory.remember_repayment_behavior(
            "bw_007", "loan_abc", "3 EMIs paid on time, 1 delayed by 2 days"
        )
        assert entry.metadata["type"] == "repayment_behavior"
