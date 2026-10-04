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


def _check_guideline_violations(copy: str, guidelines: str) -> str | None:
    """Check draft copy against negative cues and forbidden terms in guidelines."""
    gl_lower = guidelines.lower()
    if ("no emoji" in gl_lower or "avoid emoji" in gl_lower) and re.search(r"[\U00010000-\U0010ffff]", copy):
        return "contains emojis contrary to guidelines"

    forbidden = re.findall(r"(?:avoid|no|never|exclude)\s+['\"]?([a-zA-Z0-9_-]+)['\"]?", gl_lower)
    copy_lower = copy.lower()
    stopwords = {"the", "a", "an", "and", "or", "to", "in", "for"}
    for word in forbidden:
        if word not in stopwords and re.search(rf"\b{re.escape(word)}\b", copy_lower):
            return f"contains prohibited term '{word}' from guidelines"
    return None


def evaluate_brand_voice_fit(state: MarketingState) -> MarketingState:
    """Evaluate draft marketing copy against brand guidelines and tone norms.

    Args:
        state: Active Marketing state.

    Returns:
        MarketingState: State updated with brand_fit_decision ('pass' or 'revise').
    """
    if not state.draft_copy.strip():
        state.brand_fit_decision = fail_closed_check_brand_voice_fit()
        state.needs_approval = True
        state.summary = "Marketing copy is empty; revision required."
        return state

    question = build_check_brand_voice_fit_question(
        target_platform=state.platform,
        brand_guidelines=state.brand_voice_guidelines,
        post_copy=state.draft_copy,
    )
    if not question.prompt:
        state.brand_fit_decision = fail_closed_check_brand_voice_fit()
        state.needs_approval = True
        return state

    if state.platform.lower() in ("x", "twitter") and len(state.draft_copy) > 280:
        state.brand_fit_decision = "revise"
        state.summary = "Marketing copy exceeds platform length limit of 280 characters for X."
        return state

    if bool(_OFF_BRAND_PATTERNS.search(state.draft_copy)):
        state.brand_fit_decision = "revise"
        state.summary = "Marketing copy flagged: contains informal or unverified hype phrases."
        return state

    violation = _check_guideline_violations(state.draft_copy, state.brand_voice_guidelines)
    if violation:
        state.brand_fit_decision = "revise"
        state.summary = f"Marketing copy flagged: {violation}."
        return state

    state.brand_fit_decision = "pass"
    state.summary = "Marketing copy approved for tone and platform alignment."
    return state

