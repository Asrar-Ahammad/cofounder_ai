"""Report synthesis node concluding Go / Pivot / Drop recommendation."""

from packages.agents.validation.state import ValidationState


def synthesize_validation_report(state: ValidationState) -> ValidationState:
    """Synthesize final validation evaluation and recommendation.

    Args:
        state: Active Validation state.

    Returns:
        ValidationState: State updated with recommendation and summary.
    """
    if state.timing_score is None or state.problem_severity is None or state.market_size is None:
        state.recommendation = "pending"
        state.summary = "Validation evaluation pending: awaiting timing, problem severity, or market sizing."
        return state

    timing = state.timing_score.score
    severity = state.problem_severity.score
    som = state.market_size.som

    avg_score = (timing + severity) / 2.0
    if avg_score >= 7.0 and som >= 500000.0:
        rec = "go"
    elif avg_score >= 5.0:
        rec = "pivot"
    else:
        rec = "drop"

    state.recommendation = rec
    state.summary = (
        f"Validation conclusion: {rec.upper()}. "
        f"Timing: {timing:.1f}/10, Problem Severity: {severity:.1f}/10. "
        f"Calculated Year-3 SOM: ${som:,.0f}."
    )
    return state
