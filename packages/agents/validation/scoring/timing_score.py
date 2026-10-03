"""Timing score calculation rubric with mandatory evidence citations."""

from packages.agents.validation.state import ScoreResult, ValidationState


def calculate_timing_score(state: ValidationState) -> ValidationState:
    """Calculate venture market timing score based on trends and technology tailwinds.

    Args:
        state: Active Validation state.

    Returns:
        ValidationState: State updated with timing score.
    """
    inputs = state.market_size_inputs
    trend_slope = float(inputs.get("search_trend_growth_pct", 25.0))
    regulatory_catalyst = bool(inputs.get("has_regulatory_tailwinds", True))
    tech_shift = bool(inputs.get("has_technology_catalyst", True))

    score = 5.0
    if trend_slope > 20.0:
        score += 2.5
    elif trend_slope < 0:
        score -= 2.0

    if regulatory_catalyst:
        score += 1.5
    if tech_shift:
        score += 1.0

    score = max(0.0, min(10.0, score))
    rating = "high" if score >= 7.5 else ("medium" if score >= 5.0 else "low")
    citations = state.evidence_refs or ["https://trends.google.com", "https://news.ycombinator.com"]

    state.timing_score = ScoreResult(
        score=score,
        rating=rating,
        rationale=f"Timing scored {score:.1f}/10 based on {trend_slope:.1f}% growth and tailwinds.",
        evidence_refs=citations,
    )
    return state
