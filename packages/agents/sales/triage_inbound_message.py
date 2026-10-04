"""Inbound social comment and DM triage node applying Decision D13."""

import logging
import re

from packages.agents.sales.state import SalesState
from packages.core.events import DomainEvent
from packages.decisions.definitions.triage_comment_or_dm import (
    build_triage_comment_or_dm_question,
    fail_closed_triage_comment_or_dm,
)

_logger = logging.getLogger("cofunder.agents.sales.crisis")

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


def _dispatch_crisis_alert(state: SalesState) -> DomainEvent:
    """Emit high-priority crisis alert notification to the founder."""
    _logger.warning(
        "CRISIS ALERT DISPATCHED: tenant_id=%s venture_id=%s inbound=%s",
        state.tenant_id,
        state.venture_id,
        state.reply_text[:120],
    )
    return DomainEvent(
        tenant_id=state.tenant_id,
        venture_id=state.venture_id,
        type="crisis_alerted",
        payload={
            "channel": state.inbound_type,
            "prospect_email": state.prospect_email,
            "message_snippet": state.reply_text[:250],
        },
        emitted_by="sales_agent",
    )


def triage_inbound_interaction(state: SalesState) -> SalesState:
    """Triage incoming comment or DM into actionable business or crisis categories.

    Args:
        state: Active Sales state.

    Returns:
        SalesState: State updated with triage_category and crisis_alert_sent flag.
    """
    if not state.reply_text or not state.reply_text.strip():
        state.triage_category = fail_closed_triage_comment_or_dm()
        state.crisis_alert_sent = True
        state.needs_approval = True
        _dispatch_crisis_alert(state)
        state.summary = "CRISIS ALERT: Empty inbound interaction; fail-closed to crisis and alerted founder."
        return state

    question = build_triage_comment_or_dm_question(
        source_platform="social_inbox",
        message_text=state.reply_text,
    )
    if not question.prompt:
        state.triage_category = fail_closed_triage_comment_or_dm()
        state.crisis_alert_sent = True
        state.needs_approval = True
        _dispatch_crisis_alert(state)
        return state

    text_lower = state.reply_text.lower()
    if bool(_CRISIS_PATTERNS.search(text_lower)):
        state.triage_category = "crisis"
        state.crisis_alert_sent = True
        state.needs_approval = True
        _dispatch_crisis_alert(state)
        state.summary = (
            "CRISIS ALERT: High-severity legal or PR threat detected. "
            "Founder notified via urgent dispatch and automated replies blocked."
        )
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

