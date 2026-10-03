"""State definition for Market Intelligence Agent subgraph."""

from typing import Any

from pydantic import BaseModel, Field


class CompetitorProfile(BaseModel):
    """Structured competitor insight extracted from market intelligence."""

    name: str
    url: str | None = None
    positioning: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class MarketSignal(BaseModel):
    """Categorized market signal from live search or web scrape."""

    source: str
    category: str  # competitor_move, regulation, sentiment_shift, noise
    snippet: str
    confidence: float = 1.0


class MarketIntelState(BaseModel):
    """State passing through the Market Intelligence LangGraph subgraph."""

    tenant_id: str
    venture_id: str
    query: str
    search_results: list[dict[str, Any]] = Field(default_factory=list)
    signals: list[MarketSignal] = Field(default_factory=list)
    competitors: list[CompetitorProfile] = Field(default_factory=list)
    pain_points: list[dict[str, str]] = Field(default_factory=list)
    summary: str = ""
    error: str | None = None
