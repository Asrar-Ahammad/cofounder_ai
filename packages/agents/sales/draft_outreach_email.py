"""Personalized outreach drafting node for Sales Agent."""

from packages.agents.sales.state import SalesState
from packages.core.suppression import is_email_suppressed


def draft_personalized_outreach(state: SalesState) -> SalesState:
    """Generate personalized outreach email for qualified prospects.

    Args:
        state: Active Sales state.

    Returns:
        SalesState: State updated with outreach_draft and approval status.
    """
    if state.qualification_status == "disqualify":
        state.outreach_draft = ""
        state.summary = "Outreach halted: prospect does not meet qualification criteria."
        return state

    if state.prospect_email and is_email_suppressed(state.tenant_id, state.prospect_email):
        state.is_suppressed = True
        state.outreach_draft = ""
        state.summary = f"Outreach blocked: recipient '{state.prospect_email}' is on the suppression list."
        return state

    if state.qualification_status == "book_call":
        draft = (
            "Hi,\n\n"
            f"I noticed your work in {state.prospect_profile[:60]}. "
            "We're helping leaders in your space automate operational bottlenecks.\n\n"
            "Would you be open to a 15-minute introductory conversation this Thursday or Friday?\n\n"
            "Best,\nFounder"
        )
    else:
        draft = (
            "Hi,\n\n"
            "Saw your recent updates in the space. We put together a brief guide on solving common workflow friction.\n\n"
            "Let me know if you'd like me to send over the case study.\n\n"
            "Best,\nFounder"
        )

    state.outreach_draft = draft
    state.needs_approval = True
    state.summary = f"Drafted personalized outreach for {state.prospect_email}; staged for founder review."
    return state
