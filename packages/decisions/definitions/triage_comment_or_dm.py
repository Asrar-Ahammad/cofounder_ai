"""Decision D13: Inbound comment and direct message triage."""

from packages.decisions.ports import Question

TRIAGE_COMMENT_OR_DM_OPTIONS = [
    "spam",
    "lead",
    "complaint",
    "question",
    "crisis",
    "other",
]


def build_triage_comment_or_dm_question(
    source_platform: str,
    message_text: str,
) -> Question:
    """Construct Question for triaging incoming social comments or direct messages.

    Args:
        source_platform: Originating platform (e.g. 'x', 'linkedin', 'instagram').
        message_text: Inbound comment or message body.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Classify inbound message on {source_platform}: '{message_text[:300]}'. "
        "Choose category: spam (unrelated or bot), lead (sales inquiry), "
        "complaint (dissatisfaction), question (product info), or crisis (legal, security, severe PR threat)."
    )
    return Question(
        id="triage_comment_or_dm",
        prompt=prompt,
        options=TRIAGE_COMMENT_OR_DM_OPTIONS,
    )


def fail_closed_triage_comment_or_dm() -> str:
    """Return fail-closed risk rating when message triage is uncertain.

    Returns:
        str: Default to 'crisis' to halt automation and alert the founder.
    """
    return "crisis"
