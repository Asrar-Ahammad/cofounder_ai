"""Structured router node selecting next specialist agent or human intervention."""

from packages.agents.orchestrator.state import OrchestratorState


def route_next_venture_task(state: OrchestratorState) -> OrchestratorState:
    """Determine the next specialist agent to activate based on milestone progress.

    Args:
        state: Active Orchestrator state.

    Returns:
        OrchestratorState: State with next_action assigned.
    """
    # 1. If human review is pending, pause
    if state.needs_human:
        state.next_action = "human"
        return state

    # 2. Check unfinished milestones in sequence
    for m in state.milestones:
        if m.status != "completed":
            if m.id == "m1_intel":
                state.next_action = "market_intel"
                state.active_agent = "market_intel_agent"
            elif m.id == "m2_validation":
                state.next_action = "validation"
                state.active_agent = "validation_agent"
            elif m.id == "m3_financial":
                state.next_action = "financial"
                state.active_agent = "financial_agent"
            elif m.id == "m4_build":
                state.next_action = "web"
                state.active_agent = "web_agent"
            elif m.id == "m5_launch":
                state.next_action = "marketing"
                state.active_agent = "marketing_agent"
            state.summary = f"Orchestrator routed next task to '{state.next_action}' for milestone '{m.title}'."
            return state

    state.next_action = "completed"
    state.active_agent = None
    state.summary = "All registered venture milestones completed successfully."
    return state
