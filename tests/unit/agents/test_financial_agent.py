"""Unit tests for Financial Agent unit economics and constraint modeling."""

from decimal import Decimal

import pytest

from packages.agents.financial.agent import FinancialAgent
from packages.agents.financial.model_unit_economics import calculate_unit_economics
from packages.agents.financial.state import FinancialState
from packages.agents.financial.write_constraints import formulate_constraint_limits


def test_financial_unit_economics_and_constraints() -> None:
    """Verify gross margin, LTV/CAC, and break-even calculations."""
    state = FinancialState(
        tenant_id="t1",
        venture_id="v1",
        monthly_budget_cap=Decimal("2000.00"),
        fixed_overhead_monthly=Decimal("600.00"),
        target_price_monthly=Decimal("50.00"),
        estimated_cac=Decimal("100.00"),
        cogs_percentage=Decimal("20.00"),
        churn_rate_monthly=Decimal("5.00"),
    )

    state = calculate_unit_economics(state)
    assert state.metrics is not None
    # Gross margin = 80% -> $40/mo
    assert state.metrics.gross_margin_pct == Decimal("80.00")
    # Lifespan = 20 months -> LTV = $800
    assert state.metrics.ltv == Decimal("800.00")
    # LTV/CAC = 800 / 100 = 8.0x
    assert state.metrics.ltv_to_cac_ratio == Decimal("8.00")
    # Break-even = 600 / 40 = 15 customers
    assert state.metrics.break_even_customers == 15

    state = formulate_constraint_limits(state)
    assert state.constraints is not None
    assert state.constraints.budget_cap == Decimal("2000.00")
    assert state.constraints.max_cac == Decimal("125.00")


@pytest.mark.asyncio
async def test_financial_agent_graph_execution() -> None:
    """Verify Financial Agent compiled LangGraph subgraph executes end-to-end."""
    agent = FinancialAgent()
    graph = agent.build_graph()

    state = FinancialState(
        tenant_id="t1",
        venture_id="v1",
        monthly_budget_cap=Decimal("1500.00"),
    )

    final_state = await graph.ainvoke(state)
    assert final_state["metrics"] is not None
    assert final_state["constraints"] is not None
    assert "Break-even" in final_state["summary"]
