"""State definition for Financial Agent subgraph."""

from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field

from packages.core.constraints import ConstraintLimits


class UnitEconomicsMetrics(BaseModel):
    """Calculated unit economics and runway projections."""

    arpu_monthly: Decimal = Field(..., description="Average Revenue Per User per month")
    gross_margin_pct: Decimal = Field(..., description="Gross margin percentage (0-100)")
    cac: Decimal = Field(..., description="Estimated Customer Acquisition Cost")
    ltv: Decimal = Field(..., description="Customer Lifetime Value")
    ltv_to_cac_ratio: Decimal = Field(..., description="LTV / CAC ratio")
    payback_months: Decimal = Field(..., description="Months to recoup CAC")
    break_even_customers: int = Field(..., description="Paying customers needed to break even")
    runway_months: int = Field(..., description="Estimated runway based on budget cap")


class FinancialState(BaseModel):
    """State passing through the Financial LangGraph subgraph."""

    tenant_id: str
    venture_id: str
    monthly_budget_cap: Decimal = Field(..., ge=Decimal("0.00"), description="Monthly budget cap")
    fixed_overhead_monthly: Decimal = Decimal("500.00")
    target_price_monthly: Decimal = Decimal("49.00")
    estimated_cac: Decimal = Decimal("120.00")
    cogs_percentage: Decimal = Decimal("15.00")
    churn_rate_monthly: Decimal = Decimal("5.00")
    metrics: UnitEconomicsMetrics | None = None
    constraints: ConstraintLimits | None = None
    scenarios: dict[str, Any] = Field(default_factory=dict)
    assumptions: list[str] = Field(default_factory=list)
    summary: str = ""
