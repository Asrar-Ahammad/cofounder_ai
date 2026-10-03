"""Multi-scenario financial projection engine and blind-spot highlighter."""

import math
from decimal import Decimal

from packages.agents.financial.state import FinancialState


def simulate_financial_scenarios(state: FinancialState) -> FinancialState:
    """Generate best-case, base-case, and worst-case runway and unit economics scenarios.

    Args:
        state: Active Financial state.

    Returns:
        FinancialState: State updated with multi-scenario projections and identified assumptions.
    """
    base_price = state.target_price_monthly
    base_cac = state.estimated_cac
    overhead = state.fixed_overhead_monthly
    base_cogs_pct = state.cogs_percentage / Decimal("100.00")

    # 1. Base-Case Scenario
    base_margin = base_price * (Decimal("1.00") - base_cogs_pct)
    base_margin_pct = ((Decimal("1.00") - base_cogs_pct) * Decimal("100.00")).quantize(Decimal("0.01"))
    base_be = math.ceil(overhead / base_margin) if base_margin > 0 else 9999
    base_churn = state.churn_rate_monthly
    base_runway = int(state.monthly_budget_cap / overhead) if overhead > 0 else 999

    # 2. Best-Case: 20% lower CAC, 15% higher ARPU, 20% lower COGS, 30% lower churn
    best_price = (base_price * Decimal("1.15")).quantize(Decimal("0.01"))
    best_cogs = max(Decimal("0.05"), base_cogs_pct * Decimal("0.80"))
    best_margin = best_price * (Decimal("1.00") - best_cogs)
    best_margin_pct = ((Decimal("1.00") - best_cogs) * Decimal("100.00")).quantize(Decimal("0.01"))
    best_cac = (base_cac * Decimal("0.80")).quantize(Decimal("0.01"))
    best_be = math.ceil(overhead / best_margin) if best_margin > 0 else 9999
    best_churn = max(Decimal("1.00"), (base_churn * Decimal("0.70")).quantize(Decimal("0.01")))
    best_runway = int((state.monthly_budget_cap * Decimal("1.25")) / overhead) if overhead > 0 else 999

    # 3. Worst-Case: 30% higher CAC, 20% lower ARPU, 25% higher COGS, 2x churn
    worst_price = (base_price * Decimal("0.80")).quantize(Decimal("0.01"))
    worst_cogs = min(Decimal("0.90"), base_cogs_pct * Decimal("1.25"))
    worst_margin = worst_price * (Decimal("1.00") - worst_cogs)
    worst_margin_pct = ((Decimal("1.00") - worst_cogs) * Decimal("100.00")).quantize(Decimal("0.01"))
    worst_cac = (base_cac * Decimal("1.30")).quantize(Decimal("0.01"))
    worst_be = math.ceil(overhead / worst_margin) if worst_margin > 0 else 9999
    worst_churn = (base_churn * Decimal("2.00")).quantize(Decimal("0.01"))
    worst_runway = max(1, int((state.monthly_budget_cap * Decimal("0.75")) / overhead)) if overhead > 0 else 999

    state.scenarios = {
        "best_case": {
            "arpu": str(best_price),
            "cac": str(best_cac),
            "break_even_customers": best_be,
            "churn_rate_monthly": str(best_churn),
            "gross_margin_percentage": str(best_margin_pct),
            "runway_months": best_runway,
        },
        "base_case": {
            "arpu": str(base_price),
            "cac": str(base_cac),
            "break_even_customers": base_be,
            "churn_rate_monthly": str(base_churn),
            "gross_margin_percentage": str(base_margin_pct),
            "runway_months": base_runway,
        },
        "worst_case": {
            "arpu": str(worst_price),
            "cac": str(worst_cac),
            "break_even_customers": worst_be,
            "churn_rate_monthly": str(worst_churn),
            "gross_margin_percentage": str(worst_margin_pct),
            "runway_months": worst_runway,
        },
    }

    state.assumptions = [
        f"Fixed monthly overhead remains constant at ${overhead:,.2f}.",
        "Customer Acquisition Cost (CAC) assumes organic conversion without channel saturation.",
        f"Monthly churn remains steady at base {base_churn:.1f}% under normal operation.",
    ]
    return state
