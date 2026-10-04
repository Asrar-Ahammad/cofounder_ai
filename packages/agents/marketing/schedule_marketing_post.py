"""Post scheduling and staging node for Marketing Agent."""

import asyncio

from packages.agents.marketing.state import MarketingState
from packages.integrations.ports import SocialPublisher


def schedule_or_publish_post(
    state: MarketingState,
    publisher: SocialPublisher | None = None,
) -> MarketingState:
    """Stage marketing post for calendar schedule or publish subject to approval.

    Args:
        state: Active Marketing state.
        publisher: Optional SocialPublisher port adapter to trigger immediate broadcast.

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

    idemp_key = f"pub-{state.platform}-{state.venture_id[:8]}"
    if publisher is not None:
        try:
            coro = publisher.publish(
                tenant_id=state.tenant_id,
                platform=state.platform,
                text=state.draft_copy,
                media_url=state.media_url,
                idempotency_key=idemp_key,
            )
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                asyncio.create_task(coro)
            else:
                asyncio.run(coro)

            state.published_id = idemp_key
            state.summary = f"Post dispatched to {state.platform.upper()} via social publisher."
            return state
        except Exception as exc:
            state.published_id = None
            state.summary = f"Social post publication failed: {exc}"
            return state

    state.published_id = idemp_key
    state.summary = f"Post successfully queued for broadcast on {state.platform.upper()}."
    return state

