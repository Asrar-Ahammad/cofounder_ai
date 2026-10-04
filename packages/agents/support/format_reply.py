"""Customer response formatting node synthesizing grounded answers and booking options."""

from packages.agents.support.state import SupportState


def format_customer_response(state: SupportState) -> SupportState:
    """Format finalized customer-facing response text.

    Args:
        state: Active Support state.

    Returns:
        SupportState: State updated with polished response_text.
    """
    if state.requires_escalation:
        return state

    if state.routing_decision == "book_meeting" and state.booking_link:
        state.response_text = (
            "We would love to connect with you directly! Please choose a convenient time "
            f"on our calendar here: {state.booking_link}"
        )
    elif state.kb_answer:
        citation_str = f" [Ref: {', '.join(state.citations)}]" if state.citations else ""
        state.response_text = f"{state.kb_answer}{citation_str}\n\nLet us know if you need any additional details!"
    else:
        state.response_text = (
            "Thanks for reaching out! How can we assist you with our services today?"
        )

    return state
