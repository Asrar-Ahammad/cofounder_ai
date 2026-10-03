"""Report synthesis node concluding Go / Pivot / Drop recommendation."""

from packages.agents.validation.state import ValidationState


def synthesize_validation_report(state: ValidationState) -> ValidationState:
    """Synthesize final validation evaluation and recommendation.

    Args:
        state: Active Validation state.

    Returns:
        ValidationState: State updated with recommendation and summary.
    """
    timing = state.timing_score.score if state.timing_score else 5.0
    severity = state.problem_severity.score if state.problem_severity else 5.0
    som = state.market_size.som if state.market_size else 0.0

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
