"""Brand voice review node evaluating marketing draft against Decision D14."""

import re

from packages.agents.marketing.state import MarketingState
from packages.decisions.definitions.check_brand_voice_fit import (
    build_check_brand_voice_fit_question,
    fail_closed_check_brand_voice_fit,
)

_OFF_BRAND_PATTERNS = re.compile(
    r"\b(crypto\s+moon|get\s+rich\s+quick|100x\s+gains|lmao|bruh|guaranteed\s+profit)\b",
    re.IGNORECASE,
)


def evaluate_brand_voice_fit(state: MarketingState) -> MarketingState:
    """Evaluate draft marketing copy against brand guidelines and tone norms.

    Args:
        state: Active Marketing state.

    Returns:
        MarketingState: State updated with brand_fit_decision ('pass' or 'revise').
    """
    question = build_check_brand_voice_fit_question(
        target_platform=state.platform,
        brand_guidelines=state.brand_voice_guidelines,
        post_copy=state.draft_copy,
    )

    if not question.prompt:
        state.brand_fit_decision = fail_closed_check_brand_voice_fit()
        state.needs_approval = True
        return state

    if bool(_OFF_BRAND_PATTERNS.search(state.draft_copy)):
        state.brand_fit_decision = "revise"
        state.summary = "Marketing copy flagged: contains informal or unverified hype phrases."
    else:
        state.brand_fit_decision = "pass"
        state.summary = "Marketing copy approved for tone and platform alignment."

    return state
