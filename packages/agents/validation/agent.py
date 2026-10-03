"""Validation Agent implementation conforming to Agent protocol."""

from typing import Any

from packages.agents.validation.build_graph import build_validation_graph


class ValidationAgent:
    """Specialist agent calculating TAM/SAM/SOM and Go/No-Go feasibility."""

    name: str = "validation_agent"
    allowed_tools: frozenset[str] = frozenset(["web_search", "web_scrape"])
    consumes: frozenset[str] = frozenset(["market_signal_detected", "competitor_discovered"])
    emits: frozenset[str] = frozenset(["idea_validated", "validation_failed"])

    def build_graph(self) -> Any:
        """Return compiled LangGraph subgraph."""
        return build_validation_graph()
