"""Structured router node selecting next specialist agent or human intervention."""

from packages.agents.orchestrator.state import OrchestratorState

_SPECIALIST_ROUTING: dict[str, tuple[str, str]] = {
    "m1_intel": ("market_intel", "market_intel_agent"),
    "m2_validation": ("validation", "validation_agent"),
    "m3_financial": ("financial", "financial_agent"),
    "m4_build": ("web", "web_agent"),
    "m5_launch": ("marketing", "marketing_agent"),
}


def route_next_venture_task(state: OrchestratorState) -> OrchestratorState:
    """Determine the next specialist agent to activate based on milestone progress.

    Args:
        state: Active Orchestrator state.

    Returns:
        OrchestratorState: State with next_action assigned.
    """
    if state.needs_human:
        state.next_action = "human"
        return state

    for m in state.milestones:
        if m.status == "blocked":
            state.needs_human = True
            state.next_action = "human"
            state.active_agent = None
            state.summary = f"Milestone '{m.title}' is blocked; human intervention required."
            return state

        if m.status != "completed":
            routing = _SPECIALIST_ROUTING.get(m.id)
            if routing is not None:
                state.next_action, state.active_agent = routing
                state.summary = f"Orchestrator routed next task to '{state.next_action}' for milestone '{m.title}'."
            else:
                state.needs_human = True
                state.next_action = "human"
                state.active_agent = None
                state.summary = f"Unrecognized milestone '{m.id}'; routing to human review."
            return state

    state.next_action = "completed"
    state.active_agent = None
    state.summary = "All registered venture milestones completed successfully."
    return state
