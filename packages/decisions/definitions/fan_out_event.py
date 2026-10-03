"""Decision D5: Event Fan-Out Re-planning decision definition."""

from packages.decisions.ports import Question

EVENT_FANOUT_OPTIONS = ["replan_now", "replan_later", "ignore", "other"]


def build_event_fanout_question(event_type: str, event_payload_summary: str) -> Question:
    """Construct Question to decide if an incoming domain event triggers immediate re-planning.

    Args:
        event_type: Domain event identifier (e.g. 'pricing_changed', 'competitor_move').
        event_payload_summary: Concise summary of event content.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Domain event received: '{event_type}'. "
        f"Summary: {event_payload_summary[:300]}. "
        "Determine action: replan_now (critical change), replan_later (batch), ignore, or other."
    )
    return Question(
        id="fan_out_event",
        prompt=prompt,
        options=EVENT_FANOUT_OPTIONS,
    )


def fail_closed_event_fanout() -> str:
    """Return fail-safe option when event fan-out model is unavailable.

    Returns:
        str: Default to 'replan_later' to ensure event is not silently lost.
    """
    return "replan_later"
