"""Unit tests for Financial Agent scenario simulation and blind-spot highlighting."""

from decimal import Decimal

from packages.agents.financial.simulate_scenarios import simulate_financial_scenarios
from packages.agents.financial.state import FinancialState


def test_simulate_financial_scenarios_variance() -> None:
    """Verify simulation engine computes best, base, and worst case unit economics."""
    state = FinancialState(
        tenant_id="t1",
        venture_id="v1",
        monthly_budget_cap=Decimal("2000.00"),
        fixed_overhead_monthly=Decimal("600.00"),
        target_price_monthly=Decimal("50.00"),
        estimated_cac=Decimal("100.00"),
        cogs_percentage=Decimal("20.00"),
    )

    state = simulate_financial_scenarios(state)
    assert "best_case" in state.scenarios
    assert "base_case" in state.scenarios
    assert "worst_case" in state.scenarios

    best = state.scenarios["best_case"]
    base = state.scenarios["base_case"]
    worst = state.scenarios["worst_case"]

    # Best-case ARPU should be higher and CAC lower than worst-case
    assert Decimal(best["arpu"]) > Decimal(base["arpu"]) > Decimal(worst["arpu"])
    assert Decimal(best["cac"]) < Decimal(base["cac"]) < Decimal(worst["cac"])

    # Break-even customer counts
    assert best["break_even_customers"] <= base["break_even_customers"] <= worst["break_even_customers"]

    # Assumptions should be highlighted
    assert len(state.assumptions) >= 3
    assert any("CAC" in a or "Customer Acquisition Cost" in a for a in state.assumptions)
