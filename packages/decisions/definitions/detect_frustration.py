"""Decision D18: Inbound customer frustration and churn risk detection."""

from packages.decisions.ports import Question

DETECT_FRUSTRATION_OPTIONS = [
    "calm",
    "frustrated",
    "urgent_risk",
    "other",
]


def build_detect_frustration_question(
    customer_message: str,
    history_summary: str = "",
) -> Question:
    """Construct Question evaluating customer frustration and churn severity.

    Args:
        customer_message: Latest customer message text.
        history_summary: Prior conversation context summary.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Analyze customer sentiment and frustration level for message: '{customer_message[:300]}'. "
        f"Prior interaction context: '{history_summary[:200]}'. "
        "Classify into: calm (standard query/positive), frustrated (annoyed/dissatisfied), "
        "or urgent_risk (immediate churn threat, legal mention, or critical bug)."
    )
    return Question(
        id="detect_frustration",
        prompt=prompt,
        options=DETECT_FRUSTRATION_OPTIONS,
    )


def fail_closed_detect_frustration() -> str:
    """Return fail-closed rating when customer sentiment is uncertain.

    Returns:
        str: Default to 'frustrated' to prevent bot mishandling and trigger human oversight.
    """
    return "frustrated"
