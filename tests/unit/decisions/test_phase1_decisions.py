"""Unit tests for Phase 1 System One decision definitions (D3 through D10)."""

from packages.decisions.definitions.classify_founder_intent import (
    build_founder_intent_question,
    fail_closed_founder_intent,
)
from packages.decisions.definitions.fan_out_event import (
    build_event_fanout_question,
    fail_closed_event_fanout,
)
from packages.decisions.definitions.judge_trace_quality import (
    build_trace_quality_question,
    fail_closed_trace_quality,
)
from packages.decisions.definitions.route_model_tier import (
    build_model_tier_question,
    fail_closed_model_tier,
)
from packages.decisions.definitions.route_supervisor import (
    build_supervisor_routing_question,
    fail_closed_supervisor_routing,
)
from packages.decisions.definitions.select_context_to_keep import (
    build_context_compaction_question,
    fail_closed_context_compaction,
)
from packages.decisions.definitions.tag_pain_point import (
    build_pain_point_question,
    fail_closed_pain_point,
)
from packages.decisions.definitions.triage_signal import (
    build_signal_triage_question,
    fail_closed_signal_triage,
)


def test_d3_supervisor_routing() -> None:
    """Verify D3 routing options include required specialist agents and other."""
    q = build_supervisor_routing_question("Evaluate competitor pricing", "ideation")
    assert "market_intel" in q.options
    assert "validation" in q.options
    assert "financial" in q.options
    assert "other" in q.options
    assert fail_closed_supervisor_routing() == "human"


def test_d4_model_tier_routing() -> None:
    """Verify D4 tier routing options and fail-safe sonnet tier."""
    q = build_model_tier_question("Complex tax calculation", 4000)
    assert "haiku" in q.options
    assert "sonnet" in q.options
    assert "other" in q.options
    assert fail_closed_model_tier() == "sonnet"


def test_d5_event_fanout() -> None:
    """Verify D5 event fan-out options and fail-safe replan_later."""
    q = build_event_fanout_question("pricing_changed", "Price lowered to $29")
    assert "replan_now" in q.options
    assert "other" in q.options
    assert fail_closed_event_fanout() == "replan_later"


def test_d6_founder_intent() -> None:
    """Verify D6 founder intent classifier options and prompt boundary."""
    q = build_founder_intent_question("Let's focus strictly on B2B dentists")
    assert "pivot" in q.options
    assert "other" in q.options
    assert "<founder_message>" in q.prompt
    assert fail_closed_founder_intent() == "query"


def test_d7_signal_triage() -> None:
    """Verify D7 signal triage categories and fail-safe noise filter."""
    q = build_signal_triage_question("reddit", "Competitor X just laid off their team")
    assert "competitor_move" in q.options
    assert "noise" in q.options
    assert fail_closed_signal_triage() == "noise"


def test_d8_pain_point_tagging() -> None:
    """Verify D8 pain point category options."""
    q = build_pain_point_question("I hate paying $500/mo for basic features")
    assert "pricing_complaint" in q.options
    assert "missing_feature" in q.options
    assert fail_closed_pain_point() == "other"


def test_d9_trace_quality_judge() -> None:
    """Verify D9 trace judge options."""
    q = build_trace_quality_question("financial_agent", "Output calculated margins correctly")
    assert "good" in q.options
    assert "hallucination" in q.options
    assert fail_closed_trace_quality() == "incomplete"


def test_d10_context_compaction() -> None:
    """Verify D10 context compaction options."""
    q = build_context_compaction_question(180000, 200000)
    assert "summarize_older" in q.options
    assert "keep_all" in q.options
    assert fail_closed_context_compaction() == "summarize_older"
