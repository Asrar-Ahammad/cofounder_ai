"""Web copy compliance screening node applying Decision D12."""

import re

from packages.agents.web.state import WebAgentState
from packages.decisions.definitions.screen_compliance import (
    build_screen_compliance_question,
    fail_closed_screen_compliance,
)

_REGULATED_PATTERNS = re.compile(
    r"\b(guaranteed\s+(?:roi|profit|return|cure)|100%\s+risk[\-\s]*free|fda\s+approved|cure\s+all)\b",
    re.IGNORECASE,
)
_CONSENT_REQUIRED_PATTERNS = re.compile(r"""<input[^>]+type=['"]email['"]""", re.IGNORECASE)
_CONSENT_DISCLOSURE_PATTERNS = re.compile(r"\b(privacy|terms|consent|unsubscribe)\b", re.IGNORECASE)


def screen_landing_page_compliance(state: WebAgentState) -> WebAgentState:
    """Screen landing page copy for regulatory claims, missing disclosures, and consent issues.

    Args:
        state: Active Web agent state.

    Returns:
        WebAgentState: State updated with compliance_status ('clean' or specific D12 flag).
    """
    text_content = f"{state.tagline} {state.value_proposition} {state.sanitized_html}"
    question = build_screen_compliance_question("landing_page", text_content)

    if not question.prompt:
        state.compliance_status = fail_closed_screen_compliance()
        state.needs_approval = True
        return state

    content_lower = text_content.lower()
    if bool(_REGULATED_PATTERNS.search(content_lower)):
        state.compliance_status = "regulated_claim"
        state.needs_approval = True
        state.summary = "Landing page copy flagged for prohibited regulated claims."
    elif bool(_CONSENT_REQUIRED_PATTERNS.search(state.sanitized_html)) and not bool(
        _CONSENT_DISCLOSURE_PATTERNS.search(content_lower)
    ):
        state.compliance_status = "consent_issue"
        state.needs_approval = True
        state.summary = "Landing page captures email without clear privacy or consent disclosure."
    else:
        state.compliance_status = "clean"
        state.summary = "Landing page copy passed automated compliance screening."

    return state
