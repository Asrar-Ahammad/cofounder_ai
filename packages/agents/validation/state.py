"""State definition for Validation Agent subgraph."""

from typing import Any

from pydantic import BaseModel, Field


class ScoreResult(BaseModel):
    """Rubric score with transparent evidence citations."""

    score: float = Field(..., ge=0.0, le=10.0, description="Normalized score 0-10")
    rating: str = Field(..., description="'high', 'medium', or 'low'")
    rationale: str
    evidence_refs: list[str] = Field(default_factory=list, description="Mandatory citations/links")


class MarketSizeResult(BaseModel):
    """Calculated TAM, SAM, and SOM figures with formula explanation."""

    tam: float = Field(..., description="Total Addressable Market in USD")
    sam: float = Field(..., description="Serviceable Addressable Market in USD")
    som: float = Field(..., description="Serviceable Obtainable Market in USD")
    formula_explanation: str


class ValidationState(BaseModel):
    """State passing through the Validation LangGraph subgraph."""

    tenant_id: str
    venture_id: str
    idea: str
    jurisdiction: str
    market_size_inputs: dict[str, Any] = Field(default_factory=dict)
    market_size: MarketSizeResult | None = None
    timing_score: ScoreResult | None = None
    problem_severity: ScoreResult | None = None
    recommendation: str = "pending"  # go, pivot, drop
    summary: str = ""
    evidence_refs: list[str] = Field(default_factory=list)
