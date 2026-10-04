"""Gmail API email delivery adapter conforming to EmailSender port."""

import asyncio
import base64
from email.message import EmailMessage

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import EmailSender
from packages.security.egress import validate_egress_url


class GmailEmailAdapter(EmailSender):
    """Adapter for sending personalized outreach emails via Gmail API."""

    def __init__(
        self,
        oauth_token: str | None = None,
        base_url: str = "https://gmail.googleapis.com/gmail/v1/users/me",
    ) -> None:
        """Initialize Gmail email adapter.

        Args:
            oauth_token: Decrypted OAuth bearer token for the founder account.
            base_url: Base endpoint for Gmail REST API.
        """
        self.oauth_token = oauth_token
        self.base_url = base_url

    def _build_raw_mime_message(
        self,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str | None = None,
    ) -> str:
        """Build RFC 2822 MIME message encoded as URL-safe base64 without padding."""
        msg = EmailMessage()
        msg["To"] = recipient
        msg["Subject"] = subject
        msg.set_content(body_text)
        if body_html:
            msg.add_alternative(body_html, subtype="html")
        raw_bytes = msg.as_bytes()
        return base64.urlsafe_b64encode(raw_bytes).decode("utf-8").rstrip("=")

    async def send_email(
        self,
        *,
        tenant_id: str,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str | None = None,
        idempotency_key: str,
    ) -> str:
        """Send an email to a single recipient through Gmail API.

        Args:
            tenant_id: Tenant UUID string.
            recipient: Recipient email address.
            subject: Subject line.
            body_text: Plaintext email content.
            body_html: Optional HTML formatted content.
            idempotency_key: Unique idempotency key.

        Returns:
            str: Outbound email tracking or message identifier.

        Raises:
            ExternalServiceError: If sending fails or authentication expires.
        """
        if not self.oauth_token or self.oauth_token.startswith("gmail-placeholder"):
            return f"msg-simulated-{idempotency_key[:12]}"

        await asyncio.to_thread(validate_egress_url, self.base_url)
        headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json",
            "X-Tenant-Id": tenant_id,
        }
        encoded_raw = self._build_raw_mime_message(recipient, subject, body_text, body_html)
        payload = {"raw": encoded_raw}

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(f"{self.base_url}/messages/send", json=payload, headers=headers)
                res.raise_for_status()
                data = res.json()
                return str(data.get("id", idempotency_key))
        except Exception as exc:
            raise ExternalServiceError(f"Gmail API error sending to {recipient}: {exc}") from exc

