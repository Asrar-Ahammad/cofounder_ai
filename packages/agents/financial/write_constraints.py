"""Constraint generation node creating immutable boundary models."""

from decimal import Decimal

from packages.agents.financial.state import FinancialState
from packages.core.constraints import ConstraintLimits


def formulate_constraint_limits(state: FinancialState) -> FinancialState:
    """Derive versioned venture constraint limits from financial models.

    Args:
        state: Active Financial state.

    Returns:
        FinancialState: State updated with ConstraintLimits.
    """
    max_cac = state.estimated_cac * Decimal("1.25")
    limits = ConstraintLimits(
        budget_cap=state.monthly_budget_cap,
        max_cac=max_cac,
        outreach_cap=100,
    )
    state.constraints = limits
    if state.metrics:
        state.summary = (
            f"Financial Model: ${state.metrics.arpu_monthly:.2f}/mo ARPU, "
            f"{state.metrics.gross_margin_pct:.0f}% margin. "
            f"LTV/CAC: {state.metrics.ltv_to_cac_ratio:.1f}x. "
            f"Break-even at {state.metrics.break_even_customers} active customers."
        )
    return state
