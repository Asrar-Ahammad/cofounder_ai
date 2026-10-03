"""Unit economics and break-even calculation node."""

from decimal import Decimal

from packages.agents.financial.state import FinancialState, UnitEconomicsMetrics


def calculate_unit_economics(state: FinancialState) -> FinancialState:
    """Calculate margins, LTV, CAC payback, and break-even targets.

    Args:
        state: Active Financial state.

    Returns:
        FinancialState: State updated with unit economics metrics.
    """
    arpu = state.target_price_monthly
    cogs_rate = state.cogs_percentage / Decimal("100.0")
    gross_margin_dollars = arpu * (Decimal("1.0") - cogs_rate)
    gross_margin_pct = (Decimal("1.0") - cogs_rate) * Decimal("100.0")

    churn_rate = max(Decimal("0.01"), state.churn_rate_monthly / Decimal("100.0"))
    lifespan_months = Decimal("1.0") / churn_rate
    ltv = gross_margin_dollars * lifespan_months

    cac = max(Decimal("1.0"), state.estimated_cac)
    ltv_to_cac = ltv / cac
    payback_months = cac / gross_margin_dollars if gross_margin_dollars > 0 else Decimal("999")

    import math
    break_even_customers = (
        math.ceil(state.fixed_overhead_monthly / gross_margin_dollars)
        if gross_margin_dollars > 0
        else 9999
    )
    burn = state.fixed_overhead_monthly
    runway_months = int(state.monthly_budget_cap / burn) if burn > 0 else 12

    state.metrics = UnitEconomicsMetrics(
        arpu_monthly=arpu,
        gross_margin_pct=gross_margin_pct,
        cac=cac,
        ltv=ltv,
        ltv_to_cac_ratio=round(ltv_to_cac, 2),
        payback_months=round(payback_months, 1),
        break_even_customers=break_even_customers,
        runway_months=runway_months,
    )
    return state
