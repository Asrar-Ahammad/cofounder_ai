"""Decision D17: Inbound customer inquiry intent routing."""

from packages.decisions.ports import Question

ROUTE_INBOUND_MESSAGE_OPTIONS = [
    "answer_from_kb",
    "book_meeting",
    "escalate",
    "spam",
    "other",
]


def build_route_inbound_message_question(
    customer_channel: str,
    customer_message: str,
    customer_id: str = "",
) -> Question:
    """Construct Question evaluating inbound customer intent.

    Args:
        customer_channel: Channel identifier ('web', 'whatsapp').
        customer_message: Inbound customer message text.
        customer_id: Customer or session identifier.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Route customer inquiry received via {customer_channel} (customer: {customer_id}): "
        f"'{customer_message[:300]}'. Categorize into: answer_from_kb (product/service Q&A), "
        "book_meeting (schedule conversation/demo), escalate (complex, custom, or complaint), or spam."
    )
    return Question(
        id="route_inbound_message",
        prompt=prompt,
        options=ROUTE_INBOUND_MESSAGE_OPTIONS,
    )


def fail_closed_route_inbound_message() -> str:
    """Return fail-closed route when intent evaluation is uncertain.

    Returns:
        str: Default to 'escalate' to ensure human oversight.
    """
    return "escalate"
