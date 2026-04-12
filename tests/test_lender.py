"""Tests for lender management -- registration, API key auth, webhooks."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


class TestLenderRegistration:
    def test_register_lender(self, client):
        resp = client.post("/api/lender/register", json={"name": "Test NBFC"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["lender_id"].startswith("lndr_")
        assert data["api_key"].startswith("lk_")
        assert data["name"] == "Test NBFC"

    def test_register_with_segments(self, client):
        resp = client.post(
            "/api/lender/register",
            json={
                "name": "Dairy Lender",
                "segments_enabled": ["DAIRY_FARMER", "KIRANA_SHOP"],
                "max_loan_amount": 200000,
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["segments_enabled"] == ["DAIRY_FARMER", "KIRANA_SHOP"]

    def test_register_empty_name(self, client):
        resp = client.post("/api/lender/register", json={"name": ""})
        assert resp.status_code == 400

    def test_list_lenders(self, client):
        client.post("/api/lender/register", json={"name": "Lender A"})
        resp = client.get("/api/lender/list")
        assert resp.status_code == 200
        assert resp.json()["total"] >= 1


class TestLenderAuth:
    def test_profile_without_key(self, client):
        resp = client.get("/api/lender/profile")
        assert resp.status_code == 401

    def test_profile_with_invalid_key(self, client):
        resp = client.get("/api/lender/profile", headers={"X-API-Key": "invalid_key"})
        assert resp.status_code == 401

    def test_profile_with_valid_key(self, client):
        reg = client.post("/api/lender/register", json={"name": "Auth Test"})
        api_key = reg.json()["api_key"]

        resp = client.get("/api/lender/profile", headers={"X-API-Key": api_key})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Auth Test"
