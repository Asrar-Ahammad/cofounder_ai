"""Threshold policy engine mapping decision probabilities to execution bands."""

from typing import Literal

from packages.decisions.policy.hard_rules import is_never_auto
from packages.decisions.ports import Decision

ExecutionBand = Literal["AUTO", "CONFIRM", "ESCALATE"]


def apply_threshold(
    decision: Decision,
    *,
    action_name: str | None = None,
    auto_threshold: float = 0.95,
    confirm_threshold: float = 0.70,
) -> ExecutionBand:
    """Map decision choice and probabilities to an execution band.

    Args:
        decision: Evaluated Decision model.
        action_name: Optional action name to verify against never-auto hard rules.
        auto_threshold: Minimum probability required for autonomous execution.
        confirm_threshold: Minimum probability for founder confirmation before escalation.

    Returns:
        ExecutionBand: 'AUTO', 'CONFIRM', or 'ESCALATE'.
    """
    if action_name and is_never_auto(action_name):
        return "CONFIRM"

    # Reject and fail-closed choices must never execute autonomously
    if decision.choice in ("other", "block", "injection"):
        return "ESCALATE"

    # For approval risk scoring, only 'low' risk can ever be auto-approved
    if decision.question_id == "approval_risk" and decision.choice != "low":
        return "CONFIRM" if decision.choice in ("medium", "high") else "ESCALATE"

    prob = decision.probabilities.get(decision.choice, 0.0)

    if prob >= auto_threshold:
        return "AUTO"
    elif prob >= confirm_threshold:
        return "CONFIRM"
    else:
        return "ESCALATE"
