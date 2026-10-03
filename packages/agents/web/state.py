"""State definition for Web Agent landing page generation and preview deployment."""

from pydantic import BaseModel, Field


class WebAgentState(BaseModel):
    """State passing through the Web Agent LangGraph subgraph."""

    tenant_id: str
    venture_id: str
    venture_name: str
    tagline: str
    value_proposition: str
    features: list[dict[str, str]] = Field(default_factory=list)
    target_audience: str = ""
    call_to_action: str = "Join Early Access"
    generated_html: str = ""
    sanitized_html: str = ""
    compliance_status: str = "pending"  # pending, clean, flagged
    sandbox_url: str | None = None
    is_deployed: bool = False
    needs_approval: bool = True
    summary: str = ""
