"""Customer sentiment and frustration detection node applying Decision D18."""

import re

from packages.agents.support.state import SupportState
from packages.decisions.definitions.detect_frustration import (
    build_detect_frustration_question,
    fail_closed_detect_frustration,
)

_URGENT_PATTERNS = re.compile(
    r"\b(lawyer|lawsuit|sue|illegal|critical|outage|emergency|exploit|security\s+breach|cancel\s+account)\b",
    re.IGNORECASE,
)
_FRUSTRATED_PATTERNS = re.compile(
    r"\b(terrible|ridiculous|awful|unacceptable|useless|waste\s+of\s+time|angry|upset|worst|broken)\b",
    re.IGNORECASE,
)


def evaluate_customer_sentiment(state: SupportState) -> SupportState:
    """Analyze customer message for frustration or severe churn threat.

    Args:
        state: Active Support state.

    Returns:
        SupportState: State updated with frustration_level and escalation requirement.
    """
    if not state.incoming_message or not state.incoming_message.strip():
        state.frustration_level = fail_closed_detect_frustration()
        state.requires_escalation = True
        state.escalation_reason = "Empty message with uncertain sentiment; fail-closed to human review."
        return state

    question = build_detect_frustration_question(
        customer_message=state.incoming_message,
        history_summary=" ".join(state.conversation_history[-3:]),
    )
    if not question.prompt:
        state.frustration_level = fail_closed_detect_frustration()
        state.requires_escalation = True
        return state

    text_lower = state.incoming_message.lower()
    if bool(_URGENT_PATTERNS.search(text_lower)):
        state.frustration_level = "urgent_risk"
        state.requires_escalation = True
        state.escalation_reason = "Urgent legal, outage, or churn threat detected."
        state.summary = "URGENT ESCALATION: High-severity customer issue flagged for immediate founder attention."
    elif bool(_FRUSTRATED_PATTERNS.search(text_lower)):
        state.frustration_level = "frustrated"
        state.requires_escalation = True
        state.escalation_reason = "Customer expressed frustration or dissatisfaction."
        state.summary = "Customer frustration detected: routing to human founder review."
    else:
        state.frustration_level = "calm"

    return state
