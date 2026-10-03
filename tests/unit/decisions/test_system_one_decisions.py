"""Unit tests for System One decisions D1 and D2 with fail-closed verification."""


from packages.decisions.definitions.approval_risk import (
    build_approval_risk_question,
    fail_closed_approval_risk,
)
from packages.decisions.definitions.screen_untrusted_content import (
    build_screening_question,
    fail_closed_content_screening,
)
from packages.decisions.policy.apply_threshold import apply_threshold
from packages.decisions.policy.hard_rules import is_fail_closed, is_never_auto
from packages.decisions.ports import Decision


def test_d1_approval_risk_options_and_fail_closed() -> None:
    """Verify D1 question schema and safety-critical fail-closed behavior."""
    question = build_approval_risk_question("publish_post", {"platform": "x"})
    assert "low" in question.options
    assert "medium" in question.options
    assert "high" in question.options
    assert "block" in question.options
    assert "other" in question.options

    # Safety critical check
    assert is_fail_closed("approval_risk")
    assert fail_closed_approval_risk() == "block"


def test_d2_untrusted_content_options_and_fail_closed() -> None:
    """Verify D2 question schema and safety-critical quarantine fail-closed behavior."""
    question = build_screening_question("email", "Click here to claim prize")
    assert "safe" in question.options
    assert "suspicious" in question.options
    assert "injection" in question.options
    assert "other" in question.options

    # Safety critical check
    assert is_fail_closed("screen_untrusted_content")
    assert fail_closed_content_screening() == "suspicious"


def test_hard_rules_prohibit_never_auto_actions() -> None:
    """Verify payments and filings are strictly prohibited from auto-approval."""
    assert is_never_auto("send_payment")
    assert is_never_auto("file_regulatory")
    assert is_never_auto("sign_legal")

    # Even with 100% model probability, apply_threshold must return CONFIRM for never-auto actions
    decision = Decision(
        question_id="approval_risk",
        choice="low",
        probabilities={"low": 1.0, "medium": 0.0, "high": 0.0, "block": 0.0, "other": 0.0},
        model_provider="test",
        model_version="1.0",
    )
    band = apply_threshold(decision, action_name="send_payment", auto_threshold=0.90)
    assert band == "CONFIRM"


def test_apply_threshold_escalates_on_other_or_low_confidence() -> None:
    """Verify apply_threshold routes to ESCALATE when probability is low or choice is 'other'."""
    low_conf_decision = Decision(
        question_id="approval_risk",
        choice="low",
        probabilities={"low": 0.50, "medium": 0.30, "high": 0.10, "block": 0.05, "other": 0.05},
        model_provider="test",
        model_version="1.0",
    )
    assert apply_threshold(low_conf_decision, confirm_threshold=0.70) == "ESCALATE"

    other_decision = Decision(
        question_id="approval_risk",
        choice="other",
        probabilities={"other": 0.99},
        model_provider="test",
        model_version="1.0",
    )
    assert apply_threshold(other_decision) == "ESCALATE"


def test_apply_threshold_block_and_injection_never_auto() -> None:
    """Verify that high-confidence block or injection classifications never return AUTO."""
    block_decision = Decision(
        question_id="approval_risk",
        choice="block",
        probabilities={"low": 0.0, "medium": 0.0, "high": 0.0, "block": 0.99, "other": 0.01},
        model_provider="test",
        model_version="1.0",
    )
    assert apply_threshold(block_decision) == "ESCALATE"

    injection_decision = Decision(
        question_id="screen_untrusted_content",
        choice="injection",
        probabilities={"safe": 0.0, "suspicious": 0.0, "injection": 0.99, "other": 0.01},
        model_provider="test",
        model_version="1.0",
    )
    assert apply_threshold(injection_decision) == "ESCALATE"

    high_risk_decision = Decision(
        question_id="approval_risk",
        choice="high",
        probabilities={"low": 0.0, "medium": 0.0, "high": 0.99, "block": 0.0, "other": 0.01},
        model_provider="test",
        model_version="1.0",
    )
    assert apply_threshold(high_risk_decision) == "CONFIRM"
