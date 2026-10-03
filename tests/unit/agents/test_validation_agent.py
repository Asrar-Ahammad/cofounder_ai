"""Unit tests for Validation Agent market sizing and scoring rubrics."""

import pytest

from packages.agents.validation.agent import ValidationAgent
from packages.agents.validation.market_sizing import calculate_market_sizing
from packages.agents.validation.scoring.problem_severity import calculate_problem_severity
from packages.agents.validation.scoring.timing_score import calculate_timing_score
from packages.agents.validation.state import ValidationState
from packages.agents.validation.synthesize_report import synthesize_validation_report


def test_validation_market_sizing_and_rubrics() -> None:
    """Verify TAM/SAM/SOM formulas and rubric evidence citations."""
    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="Automated legal compliance for healthcare AI startups",
        jurisdiction="US-CA",
        market_size_inputs={
            "total_addressable_customers": 50000,
            "target_geography_percentage": 0.40,
            "year_3_obtainable_percentage": 0.05,
            "annual_contract_value": 2400,
            "search_trend_growth_pct": 35.0,
            "economic_pain_annual_usd": 8000.0,
        },
        evidence_refs=["https://sec.gov", "https://fda.gov"],
    )

    state = calculate_market_sizing(state)
    assert state.market_size is not None
    assert state.market_size.tam == 50000 * 2400  # $120M
    assert state.market_size.sam == 120000000 * 0.40  # $48M
    assert state.market_size.som == 48000000 * 0.05  # $2.4M

    state = calculate_timing_score(state)
    assert state.timing_score is not None
    assert state.timing_score.score >= 7.5
    assert len(state.timing_score.evidence_refs) >= 1

    state = calculate_problem_severity(state)
    assert state.problem_severity is not None
    assert state.problem_severity.score >= 7.5
    assert len(state.problem_severity.evidence_refs) >= 1

    state = synthesize_validation_report(state)
    assert state.recommendation == "go"


@pytest.mark.asyncio
async def test_validation_agent_graph_execution() -> None:
    """Verify Validation Agent LangGraph subgraph executes end-to-end."""
    agent = ValidationAgent()
    graph = agent.build_graph()

    state = ValidationState(
        tenant_id="t1",
        venture_id="v1",
        idea="SaaS billing for clinics",
        jurisdiction="US-TX",
        market_size_inputs={
            "total_addressable_customers": 10000,
            "annual_contract_value": 1200,
        },
    )

    final_state = await graph.ainvoke(state)
    assert final_state["market_size"] is not None
    assert final_state["recommendation"] in ("go", "pivot", "drop")
    assert "Validation conclusion" in final_state["summary"]
