"""Signal triage node filtering raw intelligence into structured signals."""

from packages.agents.market_intel.state import MarketIntelState, MarketSignal


def triage_raw_signals(state: MarketIntelState) -> MarketIntelState:
    """Triage raw search snippets into categorized market signals.

    Args:
        state: Active Market Intelligence state.

    Returns:
        MarketIntelState: State updated with categorized signals.
    """
    signals: list[MarketSignal] = []
    for item in state.search_results:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        combined = f"{title} {snippet}".lower()

        # Classify into signal category
        if any(term in combined for term in ("competitor", "versus", "vs", "alternative", "launch")):
            category = "competitor_move"
        elif any(term in combined for term in ("law", "compliance", "sec", "gdpr", "regulation", "fssai")):
            category = "regulation"
        elif any(term in combined for term in ("hate", "love", "trend", "shift", "surge", "problem", "expensive", "lacks")):
            category = "sentiment_shift"
        else:
            category = "noise"

        if category != "noise":
            signals.append(
                MarketSignal(
                    source=item.get("url", "web"),
                    category=category,
                    snippet=snippet,
                    confidence=0.9,
                )
            )

    state.signals = signals
    return state
