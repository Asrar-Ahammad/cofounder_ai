"""Decision D9: Agent Trace Quality Judge definition."""

from packages.decisions.ports import Question

TRACE_QUALITY_OPTIONS = [
    "good",
    "hallucination",
    "policy_violation",
    "incomplete",
    "other",
]


def build_trace_quality_question(agent_name: str, step_summary: str) -> Question:
    """Construct Question to evaluate the quality of an agent execution step.

    Args:
        agent_name: Name of the executing agent.
        step_summary: Summary of inputs, tool calls, and outputs for the step.

    Returns:
        Question: Validated Question model for automated LangSmith evaluation.
    """
    prompt = (
        f"Judge execution quality for agent '{agent_name}'. "
        f"Step summary: {step_summary[:400]}. "
        "Classify into: good, hallucination, policy_violation, incomplete, or other."
    )
    return Question(
        id="judge_trace_quality",
        prompt=prompt,
        options=TRACE_QUALITY_OPTIONS,
    )


def fail_closed_trace_quality() -> str:
    """Return fail-closed quality assessment when evaluator is down.

    Returns:
        str: Default to 'incomplete' to trigger caution in CI evals.
    """
    return "incomplete"
