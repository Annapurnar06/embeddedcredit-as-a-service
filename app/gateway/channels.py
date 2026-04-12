"""Channel adapter interface -- generic, channel-agnostic."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class IncomingMessage:
    channel: str
    channel_user_id: str
    content: str
    metadata: dict[str, Any] | None = None


@dataclass
class OutgoingMessage:
    channel: str
    channel_user_id: str
    content: str
    metadata: dict[str, Any] | None = None


class ChannelAdapter(ABC):
    @abstractmethod
    def parse_incoming(self, raw: dict[str, Any]) -> IncomingMessage: ...

    @abstractmethod
    def format_outgoing(self, message: OutgoingMessage) -> dict[str, Any]: ...


class WebChatAdapter(ChannelAdapter):
    def parse_incoming(self, raw: dict[str, Any]) -> IncomingMessage:
        return IncomingMessage(
            channel="web",
            channel_user_id=raw.get("user_id", "anonymous"),
            content=raw.get("content", ""),
            metadata=raw.get("metadata"),
        )

    def format_outgoing(self, message: OutgoingMessage) -> dict[str, Any]:
        return {
            "channel": "web",
            "user_id": message.channel_user_id,
            "content": message.content,
        }


class WhatsAppAdapter(ChannelAdapter):
    """WhatsApp BSP webhook handler -- parses standard BSP payload format."""

    def parse_incoming(self, raw: dict[str, Any]) -> IncomingMessage:
        entry = raw.get("entry", [{}])[0] if raw.get("entry") else {}
        changes = entry.get("changes", [{}])[0] if entry.get("changes") else {}
        value = changes.get("value", {})
        messages = value.get("messages", [{}])
        msg = messages[0] if messages else {}

        return IncomingMessage(
            channel="whatsapp",
            channel_user_id=msg.get("from", ""),
            content=msg.get("text", {}).get("body", ""),
            metadata={
                "message_id": msg.get("id", ""),
                "timestamp": msg.get("timestamp", ""),
                "phone_number_id": value.get("metadata", {}).get("phone_number_id", ""),
            },
        )

    def format_outgoing(self, message: OutgoingMessage) -> dict[str, Any]:
        return {
            "messaging_product": "whatsapp",
            "to": message.channel_user_id,
            "type": "text",
            "text": {"body": message.content},
        }


ADAPTERS: dict[str, ChannelAdapter] = {
    "web": WebChatAdapter(),
    "whatsapp": WhatsAppAdapter(),
}


def get_adapter(channel: str) -> ChannelAdapter:
    adapter = ADAPTERS.get(channel)
    if adapter is None:
        raise ValueError(f"Unsupported channel: {channel}")
    return adapter
