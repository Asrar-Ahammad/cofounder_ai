"""Competitor extraction node structuring rival positioning and gaps."""

from packages.agents.market_intel.state import CompetitorProfile, MarketIntelState


def extract_competitor_profiles(state: MarketIntelState) -> MarketIntelState:
    """Extract competitor landscape from search results and signals.

    Args:
        state: Active Market Intelligence state.

    Returns:
        MarketIntelState: State updated with parsed competitors.
    """
    competitors: list[CompetitorProfile] = []
    for item in state.search_results:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        # Heuristic extraction of competitor naming and positioning
        if any(term in snippet.lower() for term in ("competitor", "alternative", "platform", "tool")):
            name = title.split("-")[0].split("|")[0].strip() or "Market Incumbent"
            competitors.append(
                CompetitorProfile(
                    name=name,
                    url=item.get("url"),
                    positioning=snippet[:180],
                    strengths=["Established presence", "Domain footprint"],
                    weaknesses=["High pricing", "Complex legacy workflows"],
                )
            )

    state.competitors = competitors
    return state
