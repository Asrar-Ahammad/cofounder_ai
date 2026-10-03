"""Post scheduling and staging node for Marketing Agent."""

from packages.agents.marketing.state import MarketingState


def schedule_or_publish_post(state: MarketingState) -> MarketingState:
    """Stage marketing post for calendar schedule or publish subject to approval.

    Args:
        state: Active Marketing state.

    Returns:
        MarketingState: State updated with scheduled_time or published_id.
    """
    if state.brand_fit_decision != "pass":
        state.published_id = None
        state.summary = "Post scheduling halted: copy requires brand voice revision."
        return state

    if state.needs_approval:
        state.published_id = None
        state.summary = "Post staged in content calendar: awaiting founder approval before broadcast."
        return state

    # When approved and brand fit is confirmed
    state.published_id = f"pub-{state.platform}-{state.venture_id[:8]}"
    state.summary = f"Post successfully queued for broadcast on {state.platform.upper()}."
    return state
