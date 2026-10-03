"""Inbound social comment and DM triage node applying Decision D13."""

import re

from packages.agents.sales.state import SalesState
from packages.decisions.definitions.triage_comment_or_dm import (
    build_triage_comment_or_dm_question,
    fail_closed_triage_comment_or_dm,
)

_CRISIS_PATTERNS = re.compile(
    r"\b(lawyer|lawsuit|sue|illegal|fraud|scam|sec\s+investigation|breach|exploit|pr\s+nightmare)\b",
    re.IGNORECASE,
)
_LEAD_PATTERNS = re.compile(
    r"\b(pricing|demo|how\s+much|buy|interested|trial|enterprise)\b",
    re.IGNORECASE,
)
_SPAM_PATTERNS = re.compile(
    r"\b(follow\s+back|crypto\s+airdrop|telegram|whatsapp\s+me|check\s+bio)\b",
    re.IGNORECASE,
)


def triage_inbound_interaction(state: SalesState) -> SalesState:
    """Triage incoming comment or DM into actionable business or crisis categories.

    Args:
        state: Active Sales state.

    Returns:
        SalesState: State updated with triage_category and crisis_alert_sent flag.
    """
    question = build_triage_comment_or_dm_question(
        source_platform="social_inbox",
        message_text=state.reply_text,
    )

    if not question.prompt:
        state.triage_category = fail_closed_triage_comment_or_dm()
        state.crisis_alert_sent = True
        return state

    text_lower = state.reply_text.lower()
    if bool(_CRISIS_PATTERNS.search(text_lower)):
        state.triage_category = "crisis"
        state.crisis_alert_sent = True
        state.needs_approval = True
        state.summary = "CRISIS ALERT: High-severity legal or PR threat detected. Automated replies blocked."
    elif bool(_LEAD_PATTERNS.search(text_lower)):
        state.triage_category = "lead"
        state.summary = "Inbound sales lead detected from social interaction."
    elif bool(_SPAM_PATTERNS.search(text_lower)):
        state.triage_category = "spam"
        state.summary = "Inbound message classified as spam; dismissed from triage queue."
    else:
        state.triage_category = "question"
        state.summary = "Inbound informational question logged for response draft."

    return state
