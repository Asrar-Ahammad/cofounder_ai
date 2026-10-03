"""Unit tests for System One decisions D13 through D16."""

from packages.decisions.definitions.check_brand_voice_fit import (
    CHECK_BRAND_VOICE_FIT_OPTIONS,
    build_check_brand_voice_fit_question,
    fail_closed_check_brand_voice_fit,
)
from packages.decisions.definitions.classify_outreach_reply import (
    CLASSIFY_OUTREACH_REPLY_OPTIONS,
    build_classify_outreach_reply_question,
    fail_closed_classify_outreach_reply,
)
from packages.decisions.definitions.qualify_lead import (
    QUALIFY_LEAD_OPTIONS,
    build_qualify_lead_question,
    fail_closed_qualify_lead,
)
from packages.decisions.definitions.triage_comment_or_dm import (
    TRIAGE_COMMENT_OR_DM_OPTIONS,
    build_triage_comment_or_dm_question,
    fail_closed_triage_comment_or_dm,
)


def test_triage_comment_or_dm_decision_d13() -> None:
    """Verify D13 question schema and fail-closed crisis fallback."""
    q = build_triage_comment_or_dm_question("x", "We will sue your company for breach!")
    assert q.id == "triage_comment_or_dm"
    assert "crisis" in q.options
    assert len(q.options) == len(TRIAGE_COMMENT_OR_DM_OPTIONS)
    assert fail_closed_triage_comment_or_dm() == "crisis"


def test_check_brand_voice_fit_decision_d14() -> None:
    """Verify D14 question schema and fail-closed revise fallback."""
    q = build_check_brand_voice_fit_question("linkedin", "Authoritative B2B", "Check out our new solution.")
    assert q.id == "check_brand_voice_fit"
    assert "revise" in q.options
    assert len(q.options) == len(CHECK_BRAND_VOICE_FIT_OPTIONS)
    assert fail_closed_check_brand_voice_fit() == "revise"


def test_qualify_lead_decision_d15() -> None:
    """Verify D15 question schema and fail-closed nurture fallback."""
    q = build_qualify_lead_question("Series A CTOs", "VP of Engineering at FinTech scaleup")
    assert q.id == "qualify_lead"
    assert "book_call" in q.options
    assert len(q.options) == len(QUALIFY_LEAD_OPTIONS)
    assert fail_closed_qualify_lead() == "nurture"


def test_classify_outreach_reply_decision_d16() -> None:
    """Verify D16 question schema and fail-closed other fallback."""
    q = build_classify_outreach_reply_question("Please unsubscribe me and remove from list.")
    assert q.id == "classify_outreach_reply"
    assert "unsubscribe" in q.options
    assert len(q.options) == len(CLASSIFY_OUTREACH_REPLY_OPTIONS)
    assert fail_closed_classify_outreach_reply() == "other"
