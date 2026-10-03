"""Unit tests validating all 15 code review comment resolutions on PR #2."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from packages.agents.financial.model_unit_economics import calculate_unit_economics
from packages.agents.financial.state import FinancialState
from packages.agents.market_intel.state import MarketIntelState
from packages.agents.market_intel.triage_signal import triage_raw_signals
from packages.agents.orchestrator.agent import OrchestratorAgent
from packages.agents.orchestrator.model_milestones import (
    initialize_default_milestones,
    update_milestone_progress,
)
from packages.agents.orchestrator.route_tasks import route_next_venture_task
from packages.agents.orchestrator.state import Milestone, OrchestratorState
from packages.agents.validation.market_sizing import calculate_market_sizing
from packages.agents.validation.scoring.problem_severity import calculate_problem_severity
from packages.agents.validation.scoring.timing_score import calculate_timing_score
from packages.agents.validation.state import ValidationState
from packages.agents.validation.synthesize_report import synthesize_validation_report
from packages.core.constraints import ConstraintLimits
from packages.core.errors import ExternalServiceError, PolicyViolation
from packages.integrations.adapters.firecrawl_scraper import FirecrawlScraperAdapter


def test_break_even_customers_rounding_up() -> None:
    """Comment 1: Verify fractional break-even customers rounds up with ceil."""
    state = FinancialState(
        tenant_id="t1",
        venture_id="v1",
        monthly_budget_cap=Decimal("2000.00"),
        fixed_overhead_monthly=Decimal("601.00"),
        target_price_monthly=Decimal("50.00"),
        cogs_percentage=Decimal("20.00"),
    )
    state = calculate_unit_economics(state)
    assert state.metrics is not None
    # 601 / 40 = 15.025 -> ceil is 16
    assert state.metrics.break_even_customers == 16


def test_triage_signal_does_not_flag_security_as_regulation() -> None:
    """Comment 2: Substring 'sec' in 'security' should not trigger regulation classification."""
    state = MarketIntelState(
        tenant_id="t1",
        venture_id="v1",
        query="cybersecurity trends",
        search_results=[
            {
                "title": "Cloud Security Best Practices",
                "snippet": "Improving security posture in cloud infrastructure.",
                "url": "https://example.com/sec-posture",
            },
            {
                "title": "SEC Regulatory Enforcement Action",
                "snippet": "The SEC announced new disclosure rules.",
                "url": "https://sec.gov/news",
            },
        ],
    )
    state = triage_raw_signals(state)
    assert len(state.signals) == 1
    assert state.signals[0].category == "regulation"
    assert "sec.gov" in state.signals[0].source


def test_reopening_milestone_clears_completed_at() -> None:
    """Comment 3: Reopening a completed milestone resets completed_at to None."""
    state = OrchestratorState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="TestCo",
        idea="AI test",
        jurisdiction="US-DE",
        north_star_goal="Goal",
    )
    state = initialize_default_milestones(state)
    state = update_milestone_progress(state, "m1_intel", "completed")
    m1 = next(m for m in state.milestones if m.id == "m1_intel")
    assert m1.completed_at is not None

    state = update_milestone_progress(state, "m1_intel", "in_progress")
    assert m1.completed_at is None


def test_financial_state_rejects_negative_budget_cap() -> None:
    """Comment 4: monthly_budget_cap must reject negative values."""
    with pytest.raises(ValidationError):
        FinancialState(
            tenant_id="t1",
            venture_id="v1",
            monthly_budget_cap=Decimal("-500.00"),
        )


def test_problem_severity_parses_string_false_and_omits_fake_citations() -> None:
    """Comments 5 & 6: String 'false' does not evaluate to True, and empty citations are not faked."""
    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="Test Idea",
        jurisdiction="US-DE",
        market_size_inputs={
            "economic_pain_annual_usd": 1000.0,
            "is_daily_occurrence": "false",
            "workaround_dissatisfaction_score": 5.0,
        },
        evidence_refs=[],
    )
    state = calculate_problem_severity(state)
    assert state.problem_severity is not None
    assert state.problem_severity.evidence_refs == []
    assert "pending" in state.problem_severity.rationale.lower()
    assert state.problem_severity.score == 4.0


def test_timing_score_omits_fake_citations() -> None:
    """Comment 14: Evidence refs remain empty when none are supplied."""
    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="Test Idea",
        jurisdiction="US-DE",
        market_size_inputs={"search_trend_growth_pct": 10.0},
        evidence_refs=[],
    )
    state = calculate_timing_score(state)
    assert state.timing_score is not None
    assert state.timing_score.evidence_refs == []
    assert "pending" in state.timing_score.rationale.lower()


def test_route_tasks_handles_blocked_and_unrecognized_milestones() -> None:
    """Comments 7 & 8: Blocked milestone pauses for human; unrecognized ID routes to human."""
    state = OrchestratorState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="TestCo",
        idea="AI test",
        jurisdiction="US-DE",
        north_star_goal="Goal",
        milestones=[
            Milestone(id="m1_intel", title="Intel", stage="ideation", status="blocked"),
        ],
    )
    state = route_next_venture_task(state)
    assert state.needs_human is True
    assert state.next_action == "human"
    assert state.active_agent is None

    # Unrecognized milestone
    state.needs_human = False
    state.milestones = [
        Milestone(id="m_unknown", title="Custom", stage="custom", status="pending"),
    ]
    state = route_next_venture_task(state)
    assert state.needs_human is True
    assert state.next_action == "human"
    assert state.active_agent is None


def test_constraint_limits_is_frozen() -> None:
    """Comment 9: ConstraintLimits is immutable."""
    limits = ConstraintLimits(
        budget_cap=Decimal("1000.00"),
        max_cac=Decimal("100.00"),
        outreach_cap=50,
    )
    with pytest.raises(ValidationError):
        limits.budget_cap = Decimal("2000.00")


@pytest.mark.asyncio
async def test_firecrawl_scraper_ssrf_and_placeholder_handling() -> None:
    """Comments 10 & 11: Rejects placeholder API key, internal TLDs, and non-web ports."""
    placeholder_adapter = FirecrawlScraperAdapter(api_key="firecrawl-placeholder-key")
    with pytest.raises(ExternalServiceError, match="Firecrawl API key is missing"):
        await placeholder_adapter.scrape(url="https://example.com")

    live_adapter = FirecrawlScraperAdapter(api_key="live-key")
    with pytest.raises(PolicyViolation, match="domain is reserved for internal networks"):
        await live_adapter.scrape(url="http://service.internal/api")

    with pytest.raises(PolicyViolation, match="forbidden non-web port"):
        await live_adapter.scrape(url="http://example.com:8080/data")


def test_validation_report_pending_when_scores_incomplete() -> None:
    """Comment 12: Missing scores keep recommendation as pending."""
    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="Idea",
        jurisdiction="US-DE",
    )
    state = synthesize_validation_report(state)
    assert state.recommendation == "pending"
    assert "pending" in state.summary.lower()


def test_market_sizing_bounds_negative_and_excessive_inputs() -> None:
    """Comment 13: Clamp negative inputs and percentages > 1.0."""
    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="Idea",
        jurisdiction="US-DE",
        market_size_inputs={
            "total_addressable_customers": -100,
            "target_geography_percentage": 1.5,
            "year_3_obtainable_percentage": -0.2,
            "annual_contract_value": -50,
        },
    )
    state = calculate_market_sizing(state)
    assert state.market_size is not None
    assert state.market_size.tam == 0.0
    assert state.market_size.sam == 0.0
    assert state.market_size.som == 0.0


@pytest.mark.asyncio
async def test_orchestrator_stage_advancement() -> None:
    """Comment 15: Orchestrator evaluates stage progress across completed milestones."""
    agent = OrchestratorAgent()
    graph = agent.build_graph()

    state = OrchestratorState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="TestCo",
        idea="AI test",
        jurisdiction="US-DE",
        north_star_goal="Goal",
    )
    state = initialize_default_milestones(state)
    state = update_milestone_progress(state, "m1_intel", "completed")

    final_state = await graph.ainvoke(state)
    assert final_state["stage"] == "validation"
    assert final_state["next_action"] == "validation"
