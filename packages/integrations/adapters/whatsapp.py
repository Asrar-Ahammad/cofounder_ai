"""WhatsApp Business Cloud API messaging adapter conforming to InstantMessenger port."""

import asyncio
from typing import Any

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import InstantMessenger
from packages.security.egress import validate_egress_url


class WhatsAppCloudAdapter(InstantMessenger):
    """Adapter for sending WhatsApp messages via Meta Graph Cloud API."""

    def __init__(
        self,
        api_token: str | None = None,
        phone_number_id: str | None = None,
        base_url: str = "https://graph.facebook.com/v19.0",
    ) -> None:
        """Initialize WhatsApp Cloud adapter.

        Args:
            api_token: Meta Graph API bearer token.
            phone_number_id: Verified WhatsApp sender phone number ID.
            base_url: Base endpoint for Graph API.
        """
        self.api_token = api_token
        self.phone_number_id = phone_number_id
        self.base_url = base_url

    async def send_message(
        self,
        *,
        tenant_id: str,
        recipient_id: str,
        text: str,
        idempotency_key: str,
    ) -> str:
        """Send a WhatsApp text message to a customer or prospect.

        Args:
            tenant_id: Tenant UUID string.
            recipient_id: Customer phone number in E.164 format.
            text: Message body text.
            idempotency_key: Deterministic idempotency key.

        Returns:
            str: WhatsApp outbound message identifier (wamid).

        Raises:
            ExternalServiceError: If sending fails or authentication expires.
        """
        if not self.api_token or self.api_token.startswith("whatsapp-placeholder"):
            return f"wamid.simulated.{idempotency_key[:12]}"

        await asyncio.to_thread(validate_egress_url, self.base_url)
        sender_id = self.phone_number_id or "default"
        target_url = f"{self.base_url}/{sender_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "X-Tenant-Id": tenant_id,
        }
        payload: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(target_url, json=payload, headers=headers)
                res.raise_for_status()
                data = res.json()
                messages = data.get("messages", [])
                msg_id = messages[0].get("id") if messages else idempotency_key
                return str(msg_id)
        except Exception as exc:
            raise ExternalServiceError(f"WhatsApp API delivery failure to {recipient_id}: {exc}") from exc
