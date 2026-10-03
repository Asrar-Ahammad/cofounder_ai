"""Unit tests verifying immutable core constraint guards."""

from decimal import Decimal

import pytest

from packages.core.constraints import (
    ConstraintLimits,
    validate_cac_proposal,
    validate_outreach_proposal,
    validate_spend_proposal,
)
from packages.core.errors import PolicyViolation


def test_constraint_spend_guard() -> None:
    """Verify validate_spend_proposal blocks over-budget requests."""
    limits = ConstraintLimits(budget_cap=Decimal("1000.00"), max_cac=Decimal("150.00"), outreach_cap=100)
    # Allowed
    validate_spend_proposal(limits, 500)
    validate_spend_proposal(limits, 1000.00)

    # Exceeding budget raises PolicyViolation
    with pytest.raises(PolicyViolation, match="violates budget cap"):
        validate_spend_proposal(limits, 1000.01)


def test_constraint_cac_guard() -> None:
    """Verify validate_cac_proposal blocks high CAC campaigns."""
    limits = ConstraintLimits(budget_cap=Decimal("1000.00"), max_cac=Decimal("150.00"), outreach_cap=100)
    validate_cac_proposal(limits, 140)

    with pytest.raises(PolicyViolation, match="violates max CAC"):
        validate_cac_proposal(limits, 151)


def test_constraint_outreach_guard() -> None:
    """Verify validate_outreach_proposal blocks mass spam batches."""
    limits = ConstraintLimits(budget_cap=Decimal("1000.00"), max_cac=Decimal("150.00"), outreach_cap=100)
    validate_outreach_proposal(limits, 99)

    with pytest.raises(PolicyViolation, match="exceeds daily cap"):
        validate_outreach_proposal(limits, 101)
