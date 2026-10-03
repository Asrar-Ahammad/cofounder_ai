"""Decision D14: Marketing copy brand voice and platform fit check."""

from packages.decisions.ports import Question

CHECK_BRAND_VOICE_FIT_OPTIONS = [
    "pass",
    "revise",
    "other",
]


def build_check_brand_voice_fit_question(
    target_platform: str,
    brand_guidelines: str,
    post_copy: str,
) -> Question:
    """Construct Question evaluating draft copy against brand voice and platform norms.

    Args:
        target_platform: Target channel (e.g. 'linkedin', 'x', 'instagram').
        brand_guidelines: Summary of venture tone, style, and persona.
        post_copy: Proposed post body text.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Evaluate post copy for {target_platform} against brand guidelines ('{brand_guidelines[:150]}'): "
        f"'{post_copy[:300]}'. Determine if it passes brand voice criteria or requires revision."
    )
    return Question(
        id="check_brand_voice_fit",
        prompt=prompt,
        options=CHECK_BRAND_VOICE_FIT_OPTIONS,
    )


def fail_closed_check_brand_voice_fit() -> str:
    """Return fail-closed rating when brand voice evaluation is uncertain.

    Returns:
        str: Default to 'revise' to prevent posting off-brand content.
    """
    return "revise"
