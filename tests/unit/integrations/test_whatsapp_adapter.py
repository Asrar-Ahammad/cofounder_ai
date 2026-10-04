"""Unit tests for WhatsApp Cloud API integration adapter."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from packages.integrations.adapters.whatsapp import WhatsAppCloudAdapter


@pytest.mark.asyncio
async def test_whatsapp_adapter_simulation() -> None:
    """Verify simulation returns deterministic message ID when using placeholder key."""
    adapter = WhatsAppCloudAdapter(api_token="whatsapp-placeholder", phone_number_id="123456789")
    msg_id = await adapter.send_message(
        tenant_id="t1",
        recipient_id="+15551234567",
        text="Hello! How can we assist you?",
        idempotency_key="idemp_wa_001",
    )
    assert msg_id.startswith("wamid.simulated.")
    assert "idemp_wa_001" in msg_id


@pytest.mark.asyncio
async def test_whatsapp_adapter_real_api_call() -> None:
    """Verify WhatsApp payload construction for real Meta Graph API endpoint."""
    adapter = WhatsAppCloudAdapter(
        api_token="real_meta_token_xyz",
        phone_number_id="phone_98765",
        base_url="https://graph.facebook.com/v19.0",
    )

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = httpx.Response(
            200,
            json={"messages": [{"id": "wamid.real.meta.id.789"}]},
            request=httpx.Request("POST", "https://graph.facebook.com/v19.0/phone_98765/messages"),
        )

        msg_id = await adapter.send_message(
            tenant_id="tenant-prod",
            recipient_id="+15559876543",
            text="Your meeting is confirmed for tomorrow.",
            idempotency_key="idemp_prod_101",
        )
        assert msg_id == "wamid.real.meta.id.789"

        call_args = mock_post.call_args
        assert call_args[0][0] == "https://graph.facebook.com/v19.0/phone_98765/messages"
        payload = call_args[1]["json"]
        assert payload["messaging_product"] == "whatsapp"
        assert payload["to"] == "+15559876543"
        assert payload["text"]["body"] == "Your meeting is confirmed for tomorrow."
