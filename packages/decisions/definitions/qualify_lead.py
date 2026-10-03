"""Decision D15: Sales prospect lead qualification."""

from packages.decisions.ports import Question

QUALIFY_LEAD_OPTIONS = [
    "nurture",
    "book_call",
    "disqualify",
    "other",
]


def build_qualify_lead_question(
    target_icp: str,
    prospect_profile: str,
) -> Question:
    """Construct Question to qualify an inbound or outbound sales lead against the ICP.

    Args:
        target_icp: Ideal customer profile definition (industry, size, role).
        prospect_profile: Summary of the lead's company, title, and pain points.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Qualify sales prospect against Ideal Customer Profile ('{target_icp[:150]}'): "
        f"'{prospect_profile[:300]}'. Classify as nurture (future potential), "
        "book_call (high intent / immediate fit), or disqualify (poor fit or non-buyer)."
    )
    return Question(
        id="qualify_lead",
        prompt=prompt,
        options=QUALIFY_LEAD_OPTIONS,
    )


def fail_closed_qualify_lead() -> str:
    """Return fail-closed rating when lead qualification is uncertain.

    Returns:
        str: Default to 'nurture' to avoid dropping leads while preventing premature calls.
    """
    return "nurture"
