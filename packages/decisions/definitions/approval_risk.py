"""Decision D1: Approval Risk Scoring definition."""

from typing import Any

from packages.decisions.ports import Question

APPROVAL_RISK_OPTIONS = ["low", "medium", "high", "block", "other"]


def build_approval_risk_question(
    action: str,
    payload: dict[str, Any],
) -> Question:
    """Construct Question for assessing tool execution risk.

    Args:
        action: Name of the tool or action.
        payload: Action parameters and context.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Evaluate the operational, financial, and legal risk of executing tool '{action}' "
        f"with payload: {payload}. Classify into: low, medium, high, block, or other."
    )
    return Question(
        id="approval_risk",
        prompt=prompt,
        options=APPROVAL_RISK_OPTIONS,
    )


def fail_closed_approval_risk() -> str:
    """Return fail-closed risk rating when model is unreachable or uncalibrated.

    Returns:
        str: Default to 'block' for safety-critical protection.
    """
    return "block"
