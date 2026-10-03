"""Orchestrator Supervisor agent implementation conforming to Agent protocol."""

from typing import Any

from packages.agents.orchestrator.build_graph import build_orchestrator_graph


class OrchestratorAgent:
    """Supervisor agent coordinating specialist agents across venture milestones."""

    name: str = "orchestrator_agent"
    allowed_tools: frozenset[str] = frozenset(["read_brain", "record_decision"])
    consumes: frozenset[str] = frozenset([
        "venture_created",
        "idea_validated",
        "financial_model_created",
        "pricing_changed",
        "competitor_discovered",
    ])
    emits: frozenset[str] = frozenset([
        "milestone_started",
        "milestone_completed",
        "replan_triggered",
    ])

    def build_graph(self) -> Any:
        """Return compiled LangGraph orchestrator graph."""
        return build_orchestrator_graph()
