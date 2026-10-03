"""LangGraph subgraph compilation for Orchestrator Supervisor."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.orchestrator.model_milestones import (
    evaluate_stage_progress,
    initialize_default_milestones,
)
from packages.agents.orchestrator.route_tasks import route_next_venture_task
from packages.agents.orchestrator.state import OrchestratorState


def build_orchestrator_graph() -> Any:
    """Construct and compile the master Orchestrator Supervisor graph.

    Returns:
        CompiledStateGraph: Executable orchestrator graph.
    """
    builder = StateGraph(OrchestratorState)
    builder.add_node("initialize_milestones", initialize_default_milestones)
    builder.add_node("evaluate_stage", evaluate_stage_progress)
    builder.add_node("route_tasks", route_next_venture_task)

    builder.add_edge(START, "initialize_milestones")
    builder.add_edge("initialize_milestones", "evaluate_stage")
    builder.add_edge("evaluate_stage", "route_tasks")
    builder.add_edge("route_tasks", END)

    return builder.compile()
