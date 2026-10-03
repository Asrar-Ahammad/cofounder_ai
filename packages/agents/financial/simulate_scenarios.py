"""Multi-scenario financial projection engine and blind-spot highlighter."""

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

    # 1. Base-Case Scenario
    base_margin = base_price * (Decimal("1.00") - (state.cogs_percentage / Decimal("100.00")))
    base_be = int(overhead / base_margin) + 1 if base_margin > 0 else 9999

    # 2. Best-Case: 20% lower CAC, 15% higher ARPU
    best_price = (base_price * Decimal("1.15")).quantize(Decimal("0.01"))
    best_margin = best_price * Decimal("0.85")
    best_cac = (base_cac * Decimal("0.80")).quantize(Decimal("0.01"))
    best_be = int(overhead / best_margin) + 1 if best_margin > 0 else 9999

    # 3. Worst-Case: 30% higher CAC, 20% lower ARPU, 10% churn
    worst_price = (base_price * Decimal("0.80")).quantize(Decimal("0.01"))
    worst_margin = worst_price * Decimal("0.75")
    worst_cac = (base_cac * Decimal("1.30")).quantize(Decimal("0.01"))
    worst_be = int(overhead / worst_margin) + 1 if worst_margin > 0 else 9999

    state.scenarios = {
        "best_case": {"arpu": str(best_price), "cac": str(best_cac), "break_even_customers": best_be},
        "base_case": {"arpu": str(base_price), "cac": str(base_cac), "break_even_customers": base_be},
        "worst_case": {"arpu": str(worst_price), "cac": str(worst_cac), "break_even_customers": worst_be},
    }

    state.assumptions = [
        "Fixed monthly overhead remains constant at base projection level.",
        "Customer Acquisition Cost (CAC) assumes organic conversion without channel saturation.",
        "Monthly churn remains steady at or below 5% under baseline operations.",
    ]
    return state
