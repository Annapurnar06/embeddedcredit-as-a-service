import pytest
from httpx import ASGITransport, AsyncClient

from app.gateway.channels import WebChatAdapter, WhatsAppAdapter, get_adapter
from app.gateway.session_manager import SessionManager
from app.main import app


class TestWebAdapter:
    def test_parse(self):
        adapter = WebChatAdapter()
        msg = adapter.parse_incoming({"user_id": "u1", "content": "hello"})
        assert msg.channel == "web"
        assert msg.content == "hello"

    def test_format(self):
        from app.gateway.channels import OutgoingMessage

        adapter = WebChatAdapter()
        out = adapter.format_outgoing(
            OutgoingMessage(channel="web", channel_user_id="u1", content="hi")
        )
        assert out["content"] == "hi"


class TestWhatsAppAdapter:
    def test_parse_standard_payload(self):
        adapter = WhatsAppAdapter()
        payload = {
            "entry": [
                {
                    "changes": [
                        {
                            "value": {
                                "messages": [
                                    {
                                        "from": "919876543210",
                                        "text": {"body": "namaste"},
                                        "id": "msg123",
                                        "timestamp": "1234567890",
                                    }
                                ],
                                "metadata": {"phone_number_id": "ph123"},
                            }
                        }
                    ]
                }
            ]
        }
        msg = adapter.parse_incoming(payload)
        assert msg.channel == "whatsapp"
        assert msg.channel_user_id == "919876543210"
        assert msg.content == "namaste"

    def test_format_outgoing(self):
        from app.gateway.channels import OutgoingMessage

        adapter = WhatsAppAdapter()
        out = adapter.format_outgoing(
            OutgoingMessage(channel="whatsapp", channel_user_id="919876543210", content="hi")
        )
        assert out["messaging_product"] == "whatsapp"
        assert out["to"] == "919876543210"
        assert out["text"]["body"] == "hi"


class TestGetAdapter:
    def test_web(self):
        assert get_adapter("web") is not None

    def test_whatsapp(self):
        assert get_adapter("whatsapp") is not None

    def test_unsupported(self):
        with pytest.raises(ValueError, match="Unsupported"):
            get_adapter("telegram")


class TestSessionManager:
    def test_create_and_get(self):
        mgr = SessionManager()
        s = mgr.get_or_create("web", "u1", "L1", segment="DAIRY_FARMER")
        assert s.lender_id == "L1"
        assert s.segment == "DAIRY_FARMER"

    def test_returns_same_session(self):
        mgr = SessionManager()
        s1 = mgr.get_or_create("web", "u1", "L1")
        s2 = mgr.get_or_create("web", "u1", "L1")
        assert s1.session_id == s2.session_id

    def test_different_users(self):
        mgr = SessionManager()
        s1 = mgr.get_or_create("web", "u1", "L1")
        s2 = mgr.get_or_create("web", "u2", "L1")
        assert s1.session_id != s2.session_id

    def test_remove(self):
        mgr = SessionManager()
        mgr.get_or_create("web", "u1", "L1")
        assert mgr.active_count == 1
        mgr.remove("web", "u1", "L1")
        assert mgr.active_count == 0

    def test_count(self):
        mgr = SessionManager()
        mgr.get_or_create("web", "u1", "L1")
        mgr.get_or_create("web", "u2", "L1")
        mgr.get_or_create("whatsapp", "u1", "L1")
        assert mgr.active_count == 3


@pytest.mark.asyncio
async def test_chat_api_message():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/chat/message",
            json={
                "channel": "web",
                "channel_user_id": "test_user_1",
                "lender_id": "TEST_NBFC",
                "content": "namaste",
                "segment": "DAIRY_FARMER",
                "language": "hi",
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["state"] == "UNVERIFIED"
    assert data["response"] != ""
    assert data["channel"] == "web"


@pytest.mark.asyncio
async def test_chat_api_empty_message():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/chat/message",
            json={
                "channel": "web",
                "channel_user_id": "test_user_1",
                "lender_id": "TEST_NBFC",
                "content": "",
            },
        )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_whatsapp_webhook():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post(
            "/api/chat/webhook/whatsapp",
            json={
                "entry": [
                    {
                        "changes": [
                            {
                                "value": {
                                    "messages": [
                                        {
                                            "from": "919876543210",
                                            "text": {"body": "hello"},
                                        }
                                    ],
                                    "metadata": {},
                                }
                            }
                        ]
                    }
                ]
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "sent"
    assert data["payload"]["to"] == "919876543210"


@pytest.mark.asyncio
async def test_active_sessions_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/chat/sessions/active")
    assert resp.status_code == 200
    data = resp.json()
    assert "active_sessions" in data
