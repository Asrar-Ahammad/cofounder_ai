"""Unit tests validating all 13 code review comment resolutions on PR #4."""

import base64
import os
from email import message_from_bytes
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from packages.agents.marketing.review_brand_voice import evaluate_brand_voice_fit
from packages.agents.marketing.schedule_marketing_post import schedule_or_publish_post
from packages.agents.marketing.state import MarketingState
from packages.agents.sales.agent import SalesAgent
from packages.agents.sales.state import SalesState
from packages.agents.sales.triage_inbound_message import triage_inbound_interaction
from packages.core.config import Settings
from packages.core.suppression import (
    add_to_suppression_list,
    clear_suppression_list,
    is_email_suppressed,
    set_suppression_store_path,
)
from packages.integrations.adapters.ayrshare import AyrshareSocialAdapter
from packages.integrations.adapters.calcom import CalComCalendarAdapter
from packages.integrations.adapters.gmail import GmailEmailAdapter
from packages.security.crypto import _derive_tenant_key


@pytest.mark.asyncio
async def test_comment1_calcom_simulation_date_range() -> None:
    """Comment 1: Cal.com simulation returns slots across all days in interval."""
    adapter = CalComCalendarAdapter(api_key="calcom-placeholder")
    slots = await adapter.list_available_slots(
        tenant_id="t1",
        start_date="2026-10-10",
        end_date="2026-10-12",
    )
    # 3 days * 2 slots per day = 6 slots
    assert len(slots) == 6
    dates = {s["start_time"][:10] for s in slots}
    assert dates == {"2026-10-10", "2026-10-11", "2026-10-12"}


@pytest.mark.asyncio
async def test_comment2_3_calcom_api_parameters_and_payload() -> None:
    """Comments 2 & 3: Cal.com uses eventTypeId, ISO times, and structured responses."""
    import httpx

    adapter = CalComCalendarAdapter(api_key="real-test-key", event_type_id=42)

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = httpx.Response(
            200,
            json={"slots": [{"start_time": "2026-10-10T10:00:00Z"}]},
            request=httpx.Request("GET", "https://api.cal.com/v1/slots"),
        )

        slots = await adapter.list_available_slots(
            tenant_id="t1",
            start_date="2026-10-10",
            end_date="2026-10-11",
        )
        assert len(slots) == 1
        call_params = mock_get.call_args[1]["params"]
        assert call_params["eventTypeId"] == 42
        assert "2026-10-10T00:00:00Z" in call_params["startTime"]
        assert "2026-10-11T23:59:59Z" in call_params["endTime"]

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = httpx.Response(
            200,
            json={"booking": {"id": 101, "status": "confirmed"}},
            request=httpx.Request("POST", "https://api.cal.com/v1/bookings"),
        )

        booking = await adapter.create_booking(
            tenant_id="t1",
            attendee_email="alex@startup.io",
            attendee_name="Alex Smith",
            start_time="2026-10-10T10:00:00Z",
            idempotency_key="idemp_101",
        )
        assert booking["id"] == 101
        call_json = mock_post.call_args[1]["json"]
        assert call_json["eventTypeId"] == 42
        assert call_json["responses"] == {"email": "alex@startup.io", "name": "Alex Smith"}



def test_comment4_gmail_rfc2822_mime_encoding() -> None:
    """Comment 4: Gmail adapter encodes email as RFC 2822 MIME base64url message."""
    adapter = GmailEmailAdapter(oauth_token="test-oauth-token")
    raw_b64 = adapter._build_raw_mime_message(
        recipient="prospect@company.com",
        subject="Important Follow-up",
        body_text="Hello, here is the plaintext.",
        body_html="<p>Hello, here is the plaintext.</p>",
    )
    # Decode and parse as RFC 2822 message
    padding = "=" * (-len(raw_b64) % 4)
    raw_bytes = base64.urlsafe_b64decode(raw_b64 + padding)
    parsed = message_from_bytes(raw_bytes)

    assert parsed["To"] == "prospect@company.com"
    assert parsed["Subject"] == "Important Follow-up"
    assert parsed.is_multipart()


@pytest.mark.asyncio
async def test_comment5_ayrshare_async_egress_call() -> None:
    """Comment 5: Ayrshare publish runs egress validation asynchronously."""
    adapter = AyrshareSocialAdapter(api_key="ayrshare-placeholder")
    url = await adapter.publish(
        tenant_id="t1",
        platform="x",
        text="Launching our new product!",
        media_url=None,
        idempotency_key="idemp_x_1",
    )
    assert "https://x.com/post/simulated-" in url


def test_comment6_crypto_enforces_kms_in_production() -> None:
    """Comment 6: crypto enforces KMS master key in non-development environment."""
    prod_settings = Settings(environment="production", secret_key="dev-secret-key-at-least-32-characters-long")

    with (
        patch.dict(os.environ, {}, clear=True),
        patch("packages.security.crypto.get_settings", return_value=prod_settings),
        pytest.raises(ValueError, match="KMS master key or SECRET_KEY must be configured"),
    ):
        _derive_tenant_key("tenant-prod")


def test_comment7_adr_0007_accuracy() -> None:
    """Comment 7: ADR 0007 accurately documents Fernet and per-tenant derivation."""
    adr_path = Path("docs/decisions/0007-phase-3-go-to-market.md")
    content = adr_path.read_text(encoding="utf-8")
    assert "Fernet authenticated symmetric encryption" in content
    assert "Fernet authenticated encryption (AES-128-CBC with HMAC-SHA256)" in content


def test_comment8_review_brand_voice_guideline_and_length_checks() -> None:
    """Comment 8: review_brand_voice inspects empty copy, platform length, and guidelines."""
    # Empty copy
    state_empty = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="Acme",
        campaign_goal="Launch",
        draft_copy="   ",
    )
    state_empty = evaluate_brand_voice_fit(state_empty)
    assert state_empty.brand_fit_decision == "revise"

    # Platform length limit for X (280 chars)
    state_long = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="Acme",
        campaign_goal="Launch",
        platform="x",
        draft_copy="A" * 285,
    )
    state_long = evaluate_brand_voice_fit(state_long)
    assert state_long.brand_fit_decision == "revise"
    assert "exceeds platform length limit" in state_long.summary

    # Guideline violation: prohibited term
    state_forbidden = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="Acme",
        campaign_goal="Launch",
        platform="linkedin",
        brand_voice_guidelines="Strictly avoid synergy and buzzwords.",
        draft_copy="We provide incredible synergy for your workflow.",
    )
    state_forbidden = evaluate_brand_voice_fit(state_forbidden)
    assert state_forbidden.brand_fit_decision == "revise"
    assert "contains prohibited term 'synergy'" in state_forbidden.summary


@pytest.mark.asyncio
async def test_comment9_schedule_marketing_post_with_publisher() -> None:
    """Comment 9: schedule_or_publish_post invokes publisher when provided."""
    mock_publisher = AsyncMock()
    mock_publisher.publish.return_value = "https://linkedin.com/post/real-123"

    state = MarketingState(
        tenant_id="t1",
        venture_id="v12345678",
        venture_name="Acme",
        campaign_goal="Launch",
        platform="linkedin",
        draft_copy="Excited to announce our beta launch!",
        brand_fit_decision="pass",
        needs_approval=False,
    )

    result = schedule_or_publish_post(state, publisher=mock_publisher)
    assert result.published_id == "pub-linkedin-v1234567"
    assert "via social publisher" in result.summary
    assert mock_publisher.publish.called


@pytest.mark.asyncio
async def test_comment10_sales_agent_routes_opt_outs_in_comments_and_dms() -> None:
    """Comment 10: Inbound comments or DMs containing opt-outs route to process_reply."""
    clear_suppression_list("t1")
    agent = SalesAgent()
    graph = agent.build_graph()

    state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        inbound_type="comment",
        prospect_email="commenter@social.com",
        reply_text="Please stop contacting me and unsubscribe.",
    )

    final = await graph.ainvoke(state)
    assert final["reply_classification"] == "unsubscribe"
    assert final["is_suppressed"] is True
    assert is_email_suppressed("t1", "commenter@social.com") is True


def test_comment11_12_triage_empty_string_and_crisis_alert() -> None:
    """Comments 11 & 12: Empty interaction fail-closed to crisis and dispatches founder alert."""
    state_empty = SalesState(
        tenant_id="t1",
        venture_id="v1",
        reply_text="   ",
    )
    result = triage_inbound_interaction(state_empty)
    assert result.triage_category == "crisis"
    assert result.crisis_alert_sent is True
    assert "CRISIS ALERT" in result.summary

    state_threat = SalesState(
        tenant_id="t1",
        venture_id="v1",
        reply_text="Our company is filing a lawsuit for patent breach.",
    )
    result_threat = triage_inbound_interaction(state_threat)
    assert result_threat.triage_category == "crisis"
    assert result_threat.crisis_alert_sent is True
    assert "Founder notified via urgent dispatch" in result_threat.summary


def test_comment13_suppression_persistent_store(tmp_path: Path) -> None:
    """Comment 13: Suppression registry persists across restarts via storage backing."""
    store_file = tmp_path / "suppression_registry.json"
    set_suppression_store_path(store_file)

    add_to_suppression_list("tenant-p1", "optout@persisted.io", reason="unsubscribe")
    assert is_email_suppressed("tenant-p1", "optout@persisted.io") is True
    assert store_file.exists()

    # Simulate process restart by resetting in-memory globals and reloading
    set_suppression_store_path(None)
    clear_suppression_list("tenant-p1")
    assert is_email_suppressed("tenant-p1", "optout@persisted.io") is False

    # Re-attach persistent store file
    set_suppression_store_path(store_file)
    assert is_email_suppressed("tenant-p1", "optout@persisted.io") is True

    # Clean up
    set_suppression_store_path(None)
    clear_suppression_list()
