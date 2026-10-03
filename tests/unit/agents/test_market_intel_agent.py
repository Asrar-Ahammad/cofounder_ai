"""Unit tests for Market Intelligence Agent subgraph and nodes."""

import pytest

from packages.agents.market_intel.agent import MarketIntelAgent
from packages.agents.market_intel.analyze_competitors import extract_competitor_profiles
from packages.agents.market_intel.extract_pain_points import extract_customer_pain_points
from packages.agents.market_intel.state import MarketIntelState
from packages.agents.market_intel.triage_signal import triage_raw_signals


def test_market_intel_triage_and_competitor_extraction() -> None:
    """Verify signal triage and competitor profiling from search data."""
    state = MarketIntelState(
        tenant_id="t1",
        venture_id="v1",
        query="AI accounting for freelancers",
        search_results=[
            {
                "title": "QuickBooks - Accounting Platform",
                "url": "https://quickbooks.intuit.com",
                "snippet": "Leading competitor tool. Many users find it expensive and clunky.",
            },
            {
                "title": "IRS New 1099-K Regulation",
                "url": "https://irs.gov/news",
                "snippet": "New tax compliance law and regulation for digital payments.",
            },
        ],
    )

    state = triage_raw_signals(state)
    assert len(state.signals) == 2
    categories = [s.category for s in state.signals]
    assert "competitor_move" in categories
    assert "regulation" in categories

    state = extract_competitor_profiles(state)
    assert len(state.competitors) == 1
    assert state.competitors[0].name == "QuickBooks"

    state = extract_customer_pain_points(state)
    assert len(state.pain_points) > 0
    assert any(p["category"] == "pricing_complaint" for p in state.pain_points)


@pytest.mark.asyncio
async def test_market_intel_graph_execution() -> None:
    """Verify Market Intelligence compiled LangGraph subgraph executes end-to-end."""
    agent = MarketIntelAgent()
    graph = agent.build_graph()

    initial_state = MarketIntelState(
        tenant_id="t1",
        venture_id="v1",
        query="AI cold outreach tool",
        search_results=[
            {
                "title": "Apollo.io | Competitor platform",
                "url": "https://apollo.io",
                "snippet": "Popular sales tool, but lacks automated warm-up and is very expensive.",
            }
        ],
    )

    final_state = await graph.ainvoke(initial_state)
    assert len(final_state["competitors"]) == 1
    assert len(final_state["signals"]) >= 1
    assert "Identified" in final_state["summary"]
