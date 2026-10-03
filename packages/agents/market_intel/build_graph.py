"""LangGraph subgraph compilation for Market Intelligence agent."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.market_intel.analyze_competitors import extract_competitor_profiles
from packages.agents.market_intel.extract_pain_points import extract_customer_pain_points
from packages.agents.market_intel.state import MarketIntelState
from packages.agents.market_intel.triage_signal import triage_raw_signals


def build_market_intel_graph() -> Any:
    """Construct and compile the Market Intelligence LangGraph execution pipeline.

    Returns:
        CompiledStateGraph: Executable subgraph.
    """
    builder = StateGraph(MarketIntelState)
    builder.add_node("triage_signals", triage_raw_signals)
    builder.add_node("analyze_competitors", extract_competitor_profiles)
    builder.add_node("extract_pain_points", extract_customer_pain_points)

    builder.add_edge(START, "triage_signals")
    builder.add_edge("triage_signals", "analyze_competitors")
    builder.add_edge("analyze_competitors", "extract_pain_points")
    builder.add_edge("extract_pain_points", END)

    return builder.compile()
