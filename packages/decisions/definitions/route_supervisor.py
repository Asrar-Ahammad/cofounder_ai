"""Decision D3: Supervisor Agent Routing definition."""

from packages.decisions.ports import Question

SUPERVISOR_ROUTING_OPTIONS = [
    "market_intel",
    "validation",
    "financial",
    "legal",
    "web",
    "marketing",
    "sales",
    "support",
    "operations",
    "human",
    "other",
]


def build_supervisor_routing_question(task_description: str, venture_stage: str) -> Question:
    """Construct Question for routing next task to a specialist agent or human.

    Args:
        task_description: High-level goal or task context.
        venture_stage: Current stage of the venture (e.g. 'ideation', 'validation', 'build').

    Returns:
        Question: Validated Question model for System One router.
    """
    prompt = (
        f"Route task for venture in stage '{venture_stage}'. "
        f"Task: {task_description[:400]}. "
        "Select target specialist agent or human."
    )
    return Question(
        id="route_supervisor",
        prompt=prompt,
        options=SUPERVISOR_ROUTING_OPTIONS,
    )


def fail_closed_supervisor_routing() -> str:
    """Return fail-closed route when supervisor decision is ambiguous or model is down.

    Returns:
        str: Route to 'human' founder review to prevent unauthorized autonomous routing.
    """
    return "human"
