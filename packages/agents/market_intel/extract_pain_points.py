"""Customer pain point extraction node for Market Intelligence agent."""

from packages.agents.market_intel.state import MarketIntelState


def extract_customer_pain_points(state: MarketIntelState) -> MarketIntelState:
    """Extract actionable customer pain points and feature gaps.

    Args:
        state: Active Market Intelligence state.

    Returns:
        MarketIntelState: State updated with categorized pain points.
    """
    pain_points: list[dict[str, str]] = []
    for item in state.search_results:
        text = item.get("snippet", "").lower()
        if "expensive" in text or "cost" in text or "pricing" in text:
            pain_points.append({"category": "pricing_complaint", "evidence": item.get("snippet", "")})
        if "missing" in text or "lack" in text or "wish" in text:
            pain_points.append({"category": "missing_feature", "evidence": item.get("snippet", "")})
        if "slow" in text or "clunky" in text or "difficult" in text:
            pain_points.append({"category": "poor_ux", "evidence": item.get("snippet", "")})

    state.pain_points = pain_points
    comp_count = len(state.competitors)
    sig_count = len(state.signals)
    state.summary = (
        f"Identified {comp_count} competitors, {sig_count} actionable signals, "
        f"and {len(pain_points)} customer pain points for '{state.query}'."
    )
    return state
