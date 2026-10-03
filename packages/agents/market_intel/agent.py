"""Market Intelligence Agent implementation conforming to Agent protocol."""

from typing import Any

from packages.agents.market_intel.build_graph import build_market_intel_graph


class MarketIntelAgent:
    """Specialist agent tracking live market trends, competitors, and sentiment."""

    name: str = "market_intel_agent"
    allowed_tools: frozenset[str] = frozenset(["web_search", "web_scrape"])
    consumes: frozenset[str] = frozenset(["venture_created", "icp_updated"])
    emits: frozenset[str] = frozenset(["competitor_discovered", "market_signal_detected"])

    def build_graph(self) -> Any:
        """Return compiled LangGraph subgraph."""
        return build_market_intel_graph()
