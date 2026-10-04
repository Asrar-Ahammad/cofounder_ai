"""Unit tests for Phase 4 System One decisions D17 and D18."""

from packages.decisions.definitions.detect_frustration import (
    DETECT_FRUSTRATION_OPTIONS,
    build_detect_frustration_question,
    fail_closed_detect_frustration,
)
from packages.decisions.definitions.route_inbound_message import (
    ROUTE_INBOUND_MESSAGE_OPTIONS,
    build_route_inbound_message_question,
    fail_closed_route_inbound_message,
)


def test_decision_d17_route_inbound_message() -> None:
    """Verify D17 question formatting, options, and fail-closed safety."""
    assert "answer_from_kb" in ROUTE_INBOUND_MESSAGE_OPTIONS
    assert "book_meeting" in ROUTE_INBOUND_MESSAGE_OPTIONS
    assert "escalate" in ROUTE_INBOUND_MESSAGE_OPTIONS
    assert "spam" in ROUTE_INBOUND_MESSAGE_OPTIONS

    q = build_route_inbound_message_question(
        customer_channel="whatsapp",
        customer_message="What is the pricing for your team plan?",
        customer_id="+15551234567",
    )
    assert q.id == "route_inbound_message"
    assert "whatsapp" in q.prompt
    assert "pricing" in q.prompt
    assert fail_closed_route_inbound_message() == "escalate"


def test_decision_d18_detect_frustration() -> None:
    """Verify D18 question formatting, options, and fail-closed safety."""
    assert "calm" in DETECT_FRUSTRATION_OPTIONS
    assert "frustrated" in DETECT_FRUSTRATION_OPTIONS
    assert "urgent_risk" in DETECT_FRUSTRATION_OPTIONS

    q = build_detect_frustration_question(
        customer_message="I have been waiting 3 days and your system is completely down!",
        history_summary="Previous login failure report",
    )
    assert q.id == "detect_frustration"
    assert "completely down" in q.prompt
    assert fail_closed_detect_frustration() == "frustrated"
