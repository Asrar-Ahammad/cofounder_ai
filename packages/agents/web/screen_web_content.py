"""Web copy compliance screening node applying Decision D12."""

import re

from packages.agents.web.state import WebAgentState

# Common regulatory red-flag triggers requiring human review
_REGULATED_PATTERNS = re.compile(
    r"\b(guaranteed\s+(?:roi|profit|return|cure)|100%\s+risk[\-\s]*free|fda\s+approved|cure\s+all)\b",
    re.IGNORECASE,
)


def screen_landing_page_compliance(state: WebAgentState) -> WebAgentState:
    """Screen landing page copy for regulatory claims and consumer protection compliance.

    Args:
        state: Active Web agent state.

    Returns:
        WebAgentState: State updated with compliance_status ('clean' or 'flagged').
    """
    text_content = f"{state.tagline} {state.value_proposition} {state.sanitized_html}".lower()

    if bool(_REGULATED_PATTERNS.search(text_content)):
        state.compliance_status = "flagged"
        state.needs_approval = True
        state.summary = "Landing page copy flagged for prohibited or regulated marketing claims."
    else:
        state.compliance_status = "clean"
        state.summary = "Landing page copy passed automated compliance screening."

    return state
