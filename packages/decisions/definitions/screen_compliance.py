"""Decision D12: Content Compliance Screening Gate definition."""

from packages.decisions.ports import Question

SCREEN_COMPLIANCE_OPTIONS = [
    "clean",
    "regulated_claim",
    "missing_disclosure",
    "consent_issue",
    "other",
]


def build_screen_compliance_question(
    content_type: str,
    text_excerpt: str,
) -> Question:
    """Construct Question for screening marketing or web copy for regulatory compliance.

    Args:
        content_type: Type of public content (e.g., 'landing_page', 'outreach_email', 'ad_copy').
        text_excerpt: Sample copy or claim to evaluate.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Evaluate {content_type} text for regulatory risks (e.g., medical claims, guaranteed returns, "
        f"unlawful data collection): '{text_excerpt[:300]}'. Classify as clean, regulated_claim, "
        "missing_disclosure, consent_issue, or other."
    )
    return Question(
        id="screen_compliance",
        prompt=prompt,
        options=SCREEN_COMPLIANCE_OPTIONS,
    )


def fail_closed_screen_compliance() -> str:
    """Return fail-closed risk rating when compliance screening is uncertain.

    Returns:
        str: Default to 'regulated_claim' to require human review before publishing.
    """
    return "regulated_claim"
