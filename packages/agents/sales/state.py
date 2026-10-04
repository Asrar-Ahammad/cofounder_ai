"""State definition for Sales Agent LangGraph subgraph."""

from pydantic import BaseModel


class SalesState(BaseModel):
    """State object passing through the Sales Agent LangGraph subgraph."""

    tenant_id: str
    venture_id: str
    target_icp: str = "B2B SaaS founders and engineering leads at seed-stage startups."
    prospect_profile: str = ""
    prospect_email: str = ""
    qualification_status: str = "pending"  # 'pending', 'nurture', 'book_call', 'disqualify'
    outreach_draft: str = ""
    reply_text: str = ""
    reply_classification: str = "none"  # 'none', 'interested', 'objection', 'not_now', 'out_of_office', 'unsubscribe', 'other'
    is_suppressed: bool = False
    meeting_booked: bool = False
    inbound_type: str = "outreach"  # 'outreach', 'comment', 'dm'
    triage_category: str = "none"  # 'none', 'spam', 'lead', 'complaint', 'question', 'crisis'
    crisis_alert_sent: bool = False
    needs_approval: bool = True
    summary: str = ""
