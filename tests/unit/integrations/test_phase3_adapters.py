"""Unit tests for Ayrshare, Gmail, and Cal.com integration adapters."""

import pytest

from packages.integrations.adapters.ayrshare import AyrshareSocialAdapter
from packages.integrations.adapters.calcom import CalComCalendarAdapter
from packages.integrations.adapters.gmail import GmailEmailAdapter


@pytest.mark.asyncio
async def test_ayrshare_adapter_simulation() -> None:
    """Verify Ayrshare adapter simulation when credentials are mock/placeholder."""
    adapter = AyrshareSocialAdapter(api_key="ayrshare-placeholder")
    result = await adapter.publish(
        tenant_id="t1",
        platform="linkedin",
        text="Excited to announce our new milestone!",
        media_url=None,
        idempotency_key="idemp_1234567890ab",
    )
    assert "linkedin.com/post/simulated-" in result


@pytest.mark.asyncio
async def test_gmail_adapter_simulation() -> None:
    """Verify Gmail adapter simulation when credentials are mock/placeholder."""
    adapter = GmailEmailAdapter(oauth_token="gmail-placeholder")
    msg_id = await adapter.send_email(
        tenant_id="t1",
        recipient="lead@example.com",
        subject="Introductory chat",
        body_text="Hi, open to a quick call?",
        body_html=None,
        idempotency_key="idemp_gmail_123456",
    )
    assert msg_id.startswith("msg-simulated-")


@pytest.mark.asyncio
async def test_calcom_adapter_simulation() -> None:
    """Verify Cal.com adapter simulation for slots and bookings."""
    adapter = CalComCalendarAdapter(api_key="calcom-placeholder")
    slots = await adapter.list_available_slots(
        tenant_id="t1",
        start_date="2026-10-10",
        end_date="2026-10-12",
    )
    assert len(slots) >= 1
    assert "start_time" in slots[0]

    booking = await adapter.create_booking(
        tenant_id="t1",
        attendee_email="lead@example.com",
        attendee_name="Jane Doe",
        start_time="2026-10-10T10:00:00Z",
        idempotency_key="book_12345",
    )
    assert booking["status"] == "confirmed"
    assert "cal.com/meet/" in booking["meeting_url"]
