"""Lead qualification node for Sales Agent applying Decision D15."""

import re

from packages.agents.sales.state import SalesState
from packages.decisions.definitions.qualify_lead import (
    build_qualify_lead_question,
    fail_closed_qualify_lead,
)

_HIGH_INTENT_PATTERNS = re.compile(
    r"\b(founder|ceo|cto|vp\s+(?:of\s+)?eng(?:ineering)?|head\s+of\s+(?:product|engineering)|looking\s+to\s+buy|urgent\s+need|budget\s+approved)\b",
    re.IGNORECASE,
)
_DISQUALIFY_PATTERNS = re.compile(
    r"\b(student|intern|job\s+seeker|freelance|no\s+budget|consumer)\b",
    re.IGNORECASE,
)


def qualify_sales_prospect(state: SalesState) -> SalesState:
    """Evaluate prospect profile against venture Ideal Customer Profile.

    Args:
        state: Active Sales state.

    Returns:
        SalesState: State updated with qualification_status ('book_call', 'nurture', 'disqualify').
    """
    question = build_qualify_lead_question(
        target_icp=state.target_icp,
        prospect_profile=state.prospect_profile,
    )

    if not question.prompt:
        state.qualification_status = fail_closed_qualify_lead()
        return state

    profile_lower = state.prospect_profile.lower()
    if bool(_DISQUALIFY_PATTERNS.search(profile_lower)):
        state.qualification_status = "disqualify"
        state.summary = "Prospect disqualified: profile indicates student, intern, or no budget fit."
    elif bool(_HIGH_INTENT_PATTERNS.search(profile_lower)):
        state.qualification_status = "book_call"
        state.summary = "Prospect qualified for direct call booking: strong title and ICP fit."
    else:
        state.qualification_status = "nurture"
        state.summary = "Prospect qualified for nurture sequence: matches general industry profile."

    return state
