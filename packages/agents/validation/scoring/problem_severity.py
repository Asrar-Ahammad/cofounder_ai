"""Problem severity rubric measuring economic impact and urgency."""

from packages.agents.validation.state import ScoreResult, ValidationState


def calculate_problem_severity(state: ValidationState) -> ValidationState:
    """Evaluate customer problem severity with citation-backed evidence.

    Args:
        state: Active Validation state.

    Returns:
        ValidationState: State updated with problem severity score.
    """
    inputs = state.market_size_inputs
    budget_impact = float(inputs.get("economic_pain_annual_usd", 5000.0))
    raw_freq = inputs.get("is_daily_occurrence", True)
    frequency_daily = raw_freq is True or str(raw_freq).strip().lower() in ("true", "1", "yes")
    workaround_dissatisfaction = float(inputs.get("workaround_dissatisfaction_score", 8.0))

    score = 4.0
    if budget_impact >= 2000.0:
        score += 2.5
    if frequency_daily:
        score += 2.0
    if workaround_dissatisfaction >= 7.0:
        score += 1.5

    score = max(0.0, min(10.0, score))
    rating = "high" if score >= 7.5 else ("medium" if score >= 5.0 else "low")
    citations = list(state.evidence_refs) if state.evidence_refs else []

    freq_desc = "daily frequency" if frequency_daily else "periodic frequency"
    rationale = f"Problem severity {score:.1f}/10: ${budget_impact:,.0f} impact with {freq_desc}."
    if not citations:
        rationale += " Note: Citations are unverified/pending."

    state.problem_severity = ScoreResult(
        score=score,
        rating=rating,
        rationale=rationale,
        evidence_refs=citations,
    )
    return state
