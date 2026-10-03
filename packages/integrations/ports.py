"""Ports and abstract protocols for all external system integrations.

Business logic and agent nodes must depend exclusively on these interfaces,
never importing third-party vendor SDKs directly.
"""

from typing import Any, Protocol


class SocialPublisher(Protocol):
    """Port for publishing social media content across platforms."""

    async def publish(
        self,
        *,
        tenant_id: str,
        platform: str,
        text: str,
        media_url: str | None,
        idempotency_key: str,
    ) -> str:
        """Publish a post to the specified social network platform.

        Args:
            tenant_id: Tenant UUID string.
            platform: Platform name ('x', 'linkedin', 'facebook', 'instagram').
            text: Body text of the post.
            media_url: Optional URL to associated media file.
            idempotency_key: Unique idempotency key.

        Returns:
            str: External platform post identifier or URL.
        """
        ...


class EmailSender(Protocol):
    """Port for sending transactional and outreach emails."""

    async def send_email(
        self,
        *,
        tenant_id: str,
        recipient: str,
        subject: str,
        body_text: str,
        body_html: str | None,
        idempotency_key: str,
    ) -> str:
        """Send an email to a single recipient.

        Args:
            tenant_id: Tenant UUID string.
            recipient: Recipient email address.
            subject: Subject line of the email.
            body_text: Plaintext email content.
            body_html: Optional HTML formatted content.
            idempotency_key: Unique idempotency key.

        Returns:
            str: Outbound email tracking identifier.
        """
        ...


class WebSearcher(Protocol):
    """Port for executing web searches and trend queries."""

    async def search(
        self,
        *,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Search the public web for keyword queries.

        Args:
            query: Search query text.
            max_results: Maximum count of results to return.

        Returns:
            list[dict[str, Any]]: List of search result dictionaries containing title, url, snippet.
        """
        ...


class WebScraper(Protocol):
    """Port for extracting cleaned content from web pages."""

    async def scrape(
        self,
        *,
        url: str,
    ) -> dict[str, Any]:
        """Scrape and clean content from the specified URL.

        Args:
            url: The HTTP(S) URL to extract content from.

        Returns:
            dict[str, Any]: Extracted content with markdown text, title, and metadata.
        """
        ...


class PaymentGateway(Protocol):
    """Port for billing and subscription management."""

    async def create_checkout_session(
        self,
        *,
        tenant_id: str,
        price_id: str,
        success_url: str,
        cancel_url: str,
    ) -> str:
        """Create a hosted checkout session URL.

        Args:
            tenant_id: Tenant UUID string.
            price_id: Plan price identifier.
            success_url: Redirect URL upon success.
            cancel_url: Redirect URL upon cancellation.

        Returns:
            str: Hosted checkout URL.
        """
        ...


class CalendarScheduler(Protocol):
    """Port for calendar booking and availability synchronization."""

    async def list_available_slots(
        self,
        *,
        tenant_id: str,
        start_date: str,
        end_date: str,
    ) -> list[dict[str, Any]]:
        """List available booking slots in ISO date format.

        Args:
            tenant_id: Tenant UUID string.
            start_date: Beginning date in ISO format (YYYY-MM-DD).
            end_date: Ending date in ISO format (YYYY-MM-DD).

        Returns:
            list[dict[str, Any]]: List of slot objects containing start_time, end_time.
        """
        ...

    async def create_booking(
        self,
        *,
        tenant_id: str,
        attendee_email: str,
        attendee_name: str,
        start_time: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        """Create a confirmed calendar booking.

        Args:
            tenant_id: Tenant UUID string.
            attendee_email: Prospect or customer email.
            attendee_name: Attendee full name.
            start_time: ISO start timestamp.
            idempotency_key: Deterministic idempotency hash.

        Returns:
            dict[str, Any]: Confirmed booking details including booking_id and meeting_url.
        """
        ...
