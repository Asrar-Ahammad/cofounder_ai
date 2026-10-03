"""Prospect reply classification and immediate unsubscribe suppression node."""

import re

from packages.agents.sales.state import SalesState
from packages.core.suppression import add_to_suppression_list
from packages.decisions.definitions.classify_outreach_reply import (
    build_classify_outreach_reply_question,
    fail_closed_classify_outreach_reply,
)

_UNSUBSCRIBE_PATTERNS = re.compile(
    r"\b(unsubscribe|stop|remove\s+me|do\s+not\s+contact|opt[\s\-]*out|cease)\b",
    re.IGNORECASE,
)
_INTERESTED_PATTERNS = re.compile(
    r"\b(interested|send\s+info|demo|schedule|calendar|call|pricing|open\s+to\s+chat)\b",
    re.IGNORECASE,
)


def process_inbound_outreach_reply(state: SalesState) -> SalesState:
    """Classify prospect reply and execute immediate suppression on opt-outs.

    Args:
        state: Active Sales state.

    Returns:
        SalesState: State updated with reply classification and suppression status.
    """
    question = build_classify_outreach_reply_question(state.reply_text)
    if not question.prompt:
        state.reply_classification = fail_closed_classify_outreach_reply()
        return state

    text_lower = state.reply_text.lower()
    if bool(_UNSUBSCRIBE_PATTERNS.search(text_lower)):
        state.reply_classification = "unsubscribe"
        state.is_suppressed = True
        add_to_suppression_list(state.tenant_id, state.prospect_email, reason="unsubscribe")
        state.summary = (
            f"Prospect requested unsubscribe. Immediately added '{state.prospect_email}' "
            "to suppression list and terminated campaign."
        )
    elif bool(_INTERESTED_PATTERNS.search(text_lower)):
        state.reply_classification = "interested"
        state.summary = f"Prospect '{state.prospect_email}' expressed interest; ready for meeting booking."
    else:
        state.reply_classification = "objection"
        state.summary = f"Prospect '{state.prospect_email}' responded with questions or timing objections."

    return state
