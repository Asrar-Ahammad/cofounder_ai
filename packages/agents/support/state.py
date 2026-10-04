"""State definition for Support and Reception Agent LangGraph subgraph."""

from pydantic import BaseModel, Field


class SupportState(BaseModel):
    """State object passing through the Support Agent subgraph."""

    tenant_id: str
    venture_id: str
    customer_id: str
    channel: str = "web"  # 'web', 'whatsapp'
    incoming_message: str
    conversation_history: list[str] = Field(default_factory=list)
    approved_knowledge: dict[str, str] = Field(default_factory=dict)

    frustration_level: str = "pending"  # 'pending', 'calm', 'frustrated', 'urgent_risk'
    routing_decision: str = "pending"  # 'pending', 'answer_from_kb', 'book_meeting', 'escalate', 'spam'
    kb_answer: str = ""
    citations: list[str] = Field(default_factory=list)
    requires_escalation: bool = False
    escalation_reason: str | None = None
    response_text: str = ""
    summary: str = ""
    booking_link: str | None = None
