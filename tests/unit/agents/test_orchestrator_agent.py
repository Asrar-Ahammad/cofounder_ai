"""Unit tests for Orchestrator Supervisor routing and milestone engine."""

import pytest

from packages.agents.orchestrator.agent import OrchestratorAgent
from packages.agents.orchestrator.model_milestones import (
    initialize_default_milestones,
    update_milestone_progress,
)
from packages.agents.orchestrator.route_tasks import route_next_venture_task
from packages.agents.orchestrator.state import OrchestratorState


def test_orchestrator_milestone_progression_and_routing() -> None:
    """Verify orchestrator routes through milestones in stage order."""
    state = OrchestratorState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="Acme AI",
        idea="AI for logistics",
        jurisdiction="US-DE",
        north_star_goal="First paid pilot in 90 days",
    )

    state = initialize_default_milestones(state)
    assert len(state.milestones) == 5

    # First milestone m1_intel is in progress -> routes to market_intel
    state = route_next_venture_task(state)
    assert state.next_action == "market_intel"
    assert state.active_agent == "market_intel_agent"

    # Mark m1_intel completed -> routes to validation
    state = update_milestone_progress(state, "m1_intel", "completed")
    state = route_next_venture_task(state)
    assert state.next_action == "validation"
    assert state.active_agent == "validation_agent"

    # When needs_human is True -> pauses for founder
    state.needs_human = True
    state = route_next_venture_task(state)
    assert state.next_action == "human"


@pytest.mark.asyncio
async def test_orchestrator_agent_graph_execution() -> None:
    """Verify Orchestrator compiled LangGraph graph executes end-to-end."""
    agent = OrchestratorAgent()
    graph = agent.build_graph()

    state = OrchestratorState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="Acme AI",
        idea="AI for logistics",
        jurisdiction="US-DE",
        north_star_goal="First paid pilot in 90 days",
    )

    final_state = await graph.ainvoke(state)
    assert len(final_state["milestones"]) == 5
    assert final_state["next_action"] == "market_intel"
