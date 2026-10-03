"""Core hard constraint checks enforcing immutable business boundaries."""

from decimal import Decimal

from pydantic import BaseModel, Field

from packages.core.errors import PolicyViolation


class ConstraintLimits(BaseModel):
    """Immutable business boundaries configured for a venture."""

    budget_cap: Decimal = Field(..., ge=0, description="Monthly spending ceiling")
    max_cac: Decimal = Field(..., ge=0, description="Maximum customer acquisition cost ceiling")
    outreach_cap: int = Field(..., ge=0, description="Daily outbound message volume cap")


def validate_spend_proposal(limits: ConstraintLimits, requested_amount: Decimal | float) -> None:
    """Enforce spending does not exceed the venture's monthly budget cap.

    Args:
        limits: Active venture constraint boundaries.
        requested_amount: Proposed spending amount.

    Raises:
        PolicyViolation: If proposal exceeds the configured budget cap.
    """
    amount = Decimal(str(requested_amount))
    if amount > limits.budget_cap:
        raise PolicyViolation(
            f"Spend proposal of ${amount:.2f} violates budget cap of ${limits.budget_cap:.2f}"
        )


def validate_cac_proposal(limits: ConstraintLimits, estimated_cac: Decimal | float) -> None:
    """Enforce estimated customer acquisition cost does not exceed CAC ceiling.

    Args:
        limits: Active venture constraint boundaries.
        estimated_cac: Projected CAC for the campaign.

    Raises:
        PolicyViolation: If estimated CAC exceeds ceiling.
    """
    cac = Decimal(str(estimated_cac))
    if cac > limits.max_cac:
        raise PolicyViolation(
            f"Campaign CAC of ${cac:.2f} violates max CAC threshold of ${limits.max_cac:.2f}"
        )


def validate_outreach_proposal(limits: ConstraintLimits, target_count: int) -> None:
    """Enforce outbound volume does not exceed daily messaging cap.

    Args:
        limits: Active venture constraint boundaries.
        target_count: Number of recipients in proposed outreach batch.

    Raises:
        PolicyViolation: If count exceeds cap.
    """
    if target_count > limits.outreach_cap:
        raise PolicyViolation(
            f"Outreach batch of {target_count} exceeds daily cap of {limits.outreach_cap}"
        )
