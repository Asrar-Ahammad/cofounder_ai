"""Decision D16: Prospect outreach reply classification."""

from packages.decisions.ports import Question

CLASSIFY_OUTREACH_REPLY_OPTIONS = [
    "interested",
    "objection",
    "not_now",
    "out_of_office",
    "unsubscribe",
    "other",
]


def build_classify_outreach_reply_question(
    reply_body: str,
) -> Question:
    """Construct Question to classify the sentiment and intent of an outreach reply.

    Args:
        reply_body: Prospect reply email or message text.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Classify outreach reply intent: '{reply_body[:300]}'. Choose one category: "
        "interested (wants demo or more info), objection (pushback on pricing/features), "
        "not_now (follow up later), out_of_office (automated auto-responder), "
        "unsubscribe (request to stop contacting or remove from list), or other."
    )
    return Question(
        id="classify_outreach_reply",
        prompt=prompt,
        options=CLASSIFY_OUTREACH_REPLY_OPTIONS,
    )


def fail_closed_classify_outreach_reply() -> str:
    """Return fail-closed classification when reply intent is ambiguous.

    Returns:
        str: Default to 'other' requiring manual inbox review.
    """
    return "other"
