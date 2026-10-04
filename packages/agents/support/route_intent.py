"""Customer message intent routing node applying Decision D17."""

import re

from packages.agents.support.state import SupportState
from packages.decisions.definitions.route_inbound_message import (
    build_route_inbound_message_question,
    fail_closed_route_inbound_message,
)

_SPAM_PATTERNS = re.compile(
    r"\b(crypto\s+airdrop|telegram|follow\s+back|buy\s+followers|casino|forex|click\s+here)\b",
    re.IGNORECASE,
)
_MEETING_PATTERNS = re.compile(
    r"\b(book|schedule|demo|meeting|call|calendar|speak\s+to|intro\s+call)\b",
    re.IGNORECASE,
)
_ESCALATE_PATTERNS = re.compile(
    r"\b(enterprise\s+contract|custom\s+terms|partnership|nda|investor|press|complaint)\b",
    re.IGNORECASE,
)


def route_customer_intent(state: SupportState) -> SupportState:
    """Classify customer message into actionable service pathways.

    Args:
        state: Active Support state.

    Returns:
        SupportState: State updated with routing_decision.
    """
    question = build_route_inbound_message_question(
        customer_channel=state.channel,
        customer_message=state.incoming_message,
        customer_id=state.customer_id,
    )
    if not question.prompt:
        state.routing_decision = fail_closed_route_inbound_message()
        state.requires_escalation = True
        return state

    text_lower = state.incoming_message.lower()
    if bool(_SPAM_PATTERNS.search(text_lower)):
        state.routing_decision = "spam"
        state.summary = "Inbound message identified as spam; dismissed from support queue."
    elif bool(_MEETING_PATTERNS.search(text_lower)):
        state.routing_decision = "book_meeting"
        state.booking_link = f"https://cal.com/founder/{state.venture_id[:8]}"
        state.summary = "Customer requested meeting; meeting scheduler booking link prepared."
    elif bool(_ESCALATE_PATTERNS.search(text_lower)):
        state.routing_decision = "escalate"
        state.requires_escalation = True
        state.escalation_reason = "Inquiry requires founder or executive decision."
        state.summary = "Custom or enterprise inquiry routed for human escalation."
    else:
        state.routing_decision = "answer_from_kb"
        state.summary = "Inquiry classified for grounded knowledge base Q&A resolution."

    return state
