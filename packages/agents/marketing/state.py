"""State definition for Marketing and Social Agent LangGraph subgraph."""

from pydantic import BaseModel, Field


class MarketingState(BaseModel):
    """State object passing through the Marketing Agent subgraph."""

    tenant_id: str
    venture_id: str
    venture_name: str
    campaign_goal: str
    target_audience: str = ""
    brand_voice_guidelines: str = "Professional, authoritative, transparent, and founder-focused."
    platform: str = "linkedin"  # 'linkedin', 'x', 'instagram', 'facebook'
    draft_copy: str = ""
    media_url: str | None = None
    brand_fit_decision: str = "pending"  # 'pending', 'pass', 'revise'
    scheduled_time: str | None = None
    published_id: str | None = None
    needs_approval: bool = True
    summary: str = ""
    tags: list[str] = Field(default_factory=list)

