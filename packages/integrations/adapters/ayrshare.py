"""Ayrshare multi-platform social publishing adapter conforming to SocialPublisher port."""

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import SocialPublisher
from packages.security.egress import validate_egress_url


class AyrshareSocialAdapter(SocialPublisher):
    """Adapter publishing posts across social networks via Ayrshare API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.ayrshare.com/api",
    ) -> None:
        """Initialize Ayrshare adapter with credentials.

        Args:
            api_key: Ayrshare API key or JWT token.
            base_url: Base endpoint for Ayrshare REST API.
        """
        self.api_key = api_key
        self.base_url = base_url

    async def publish(
        self,
        *,
        tenant_id: str,
        platform: str,
        text: str,
        media_url: str | None = None,
        idempotency_key: str,
    ) -> str:
        """Publish a post to the specified social network.

        Args:
            tenant_id: Tenant UUID string.
            platform: Social platform ('x', 'linkedin', 'facebook', 'instagram').
            text: Post body text.
            media_url: Optional media attachment URL.
            idempotency_key: Unique idempotency key.

        Returns:
            str: External platform post identifier or URL.

        Raises:
            ExternalServiceError: If publishing fails or network errors occur.
        """
        if not self.api_key or self.api_key.startswith("ayrshare-placeholder"):
            return f"https://{platform}.com/post/simulated-{idempotency_key[:12]}"

        validate_egress_url(self.base_url)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Tenant-Id": tenant_id,
            "X-Idempotency-Key": idempotency_key,
        }
        payload = {
            "post": text,
            "platforms": [platform.lower()],
            "mediaUrls": [media_url] if media_url else [],
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(f"{self.base_url}/post", json=payload, headers=headers)
                res.raise_for_status()
                data = res.json()
                post_id = str(data.get("id") or data.get("postIds", {}).get(platform, idempotency_key))
                return f"https://{platform}.com/post/{post_id}"
        except Exception as exc:
            raise ExternalServiceError(f"Ayrshare API error on {platform}: {exc}") from exc
