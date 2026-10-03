"""North-star milestone engine evaluating milestone progress and stage transitions."""

from datetime import UTC, datetime

from packages.agents.orchestrator.state import Milestone, OrchestratorState


def initialize_default_milestones(state: OrchestratorState) -> OrchestratorState:
    """Initialize standard venture milestones if none exist.

    Args:
        state: Active Orchestrator state.

    Returns:
        OrchestratorState: State initialized with default milestones.
    """
    if not state.milestones:
        state.milestones = [
            Milestone(id="m1_intel", title="Market Intelligence Dossier", stage="ideation", status="in_progress"),
            Milestone(id="m2_validation", title="TAM/SAM/SOM & Feasibility Scored", stage="validation", status="pending"),
            Milestone(id="m3_financial", title="Unit Economics & Budget Limits", stage="validation", status="pending"),
            Milestone(id="m4_build", title="Landing Page & MVP Prototype", stage="build", status="pending"),
            Milestone(id="m5_launch", title="GTM Campaign & Outreach", stage="gtm", status="pending"),
        ]
    return state


def update_milestone_progress(state: OrchestratorState, milestone_id: str, status: str) -> OrchestratorState:
    """Update progress for a specific milestone.

    Args:
        state: Active Orchestrator state.
        milestone_id: Target milestone identifier.
        status: Updated status ('in_progress', 'completed', 'blocked').

    Returns:
        OrchestratorState: Updated state.
    """
    now_iso = datetime.now(UTC).isoformat()
    for m in state.milestones:
        if m.id == milestone_id:
            m.status = status
            if status == "completed":
                m.completed_at = now_iso
            else:
                m.completed_at = None
            break
    return state


def evaluate_stage_progress(state: OrchestratorState) -> OrchestratorState:
    """Evaluate milestone progress to advance or align the venture stage.

    Args:
        state: Active Orchestrator state.

    Returns:
        OrchestratorState: State updated with the current venture stage.
    """
    if not state.milestones:
        return state

    for m in state.milestones:
        if m.status != "completed":
            state.stage = m.stage
            return state

    state.stage = "scale"
    return state
