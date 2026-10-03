"""Financial Agent implementation conforming to Agent protocol."""

from typing import Any

from packages.agents.financial.build_graph import build_financial_graph


class FinancialAgent:
    """Specialist agent modeling unit economics, pricing, and spend boundaries."""

    name: str = "financial_agent"
    allowed_tools: frozenset[str] = frozenset(["read_brain", "record_decision", "write_constraint"])
    consumes: frozenset[str] = frozenset(["idea_validated", "pricing_changed"])
    emits: frozenset[str] = frozenset(["financial_model_created", "budget_constraint_changed"])

    def build_graph(self) -> Any:
        """Return compiled LangGraph subgraph."""
        return build_financial_graph()
