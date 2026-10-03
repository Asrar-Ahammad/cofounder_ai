"""Unit tests for Phase 2 System One Decisions D11 and D12."""

from packages.decisions.definitions.gate_legal_answer import (
    GATE_LEGAL_OPTIONS,
    build_gate_legal_question,
    fail_closed_gate_legal_answer,
)
from packages.decisions.definitions.screen_compliance import (
    SCREEN_COMPLIANCE_OPTIONS,
    build_screen_compliance_question,
    fail_closed_screen_compliance,
)


def test_decision_d11_gate_legal_answer() -> None:
    """Verify D11 Question construction and fail-closed safety default."""
    q = build_gate_legal_question(
        query="What are the data consent requirements in India?",
        top_score=0.85,
        top_citation="DPDP Act Section 6",
    )
    assert q.id == "gate_legal_answer"
    assert "DPDP Act Section 6" in q.prompt
    assert q.options == GATE_LEGAL_OPTIONS
    assert "abstain" in q.options

    # Fail closed must be abstain to prevent hallucinated legal advice
    assert fail_closed_gate_legal_answer() == "abstain"


def test_decision_d12_screen_compliance() -> None:
    """Verify D12 Question construction and fail-closed safety default."""
    q = build_screen_compliance_question(
        content_type="landing_page",
        text_excerpt="Guaranteed 100% ROI in 30 days without risk.",
    )
    assert q.id == "screen_compliance"
    assert "landing_page" in q.prompt
    assert q.options == SCREEN_COMPLIANCE_OPTIONS
    assert "regulated_claim" in q.options

    # Fail closed must be regulated_claim to require human review
    assert fail_closed_screen_compliance() == "regulated_claim"
