"""Support escalation node alerting the founder and generating customer holding response."""

import logging

from packages.agents.support.state import SupportState
from packages.core.events import DomainEvent

_logger = logging.getLogger("cofunder.agents.support.escalation")


def escalate_to_founder(state: SupportState) -> SupportState:
    """Escalate customer issue to founder inbox and prepare customer notification.

    Args:
        state: Active Support state.

    Returns:
        SupportState: State updated with holding response and escalation event.
    """
    state.requires_escalation = True
    reason = state.escalation_reason or "Customer inquiry requires executive assistance."

    _logger.warning(
        "SUPPORT ESCALATION: tenant_id=%s venture_id=%s customer=%s reason=%s",
        state.tenant_id,
        state.venture_id,
        state.customer_id,
        reason,
    )

    # Emit domain event for worker notifications
    DomainEvent(
        tenant_id=state.tenant_id,
        venture_id=state.venture_id,
        type="support_escalated",
        payload={
            "customer_id": state.customer_id,
            "channel": state.channel,
            "reason": reason,
            "message_snippet": state.incoming_message[:250],
            "frustration_level": state.frustration_level,
        },
        emitted_by="support_agent",
    )

    state.response_text = (
        "Thank you for contacting us. I have directly escalated your request to our founder "
        "and senior team for personalized review. We will follow up with you shortly."
    )
    state.summary = f"Ticket escalated to founder inbox. Reason: {reason}."
    return state
