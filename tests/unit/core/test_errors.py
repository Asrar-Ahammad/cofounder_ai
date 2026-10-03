"""Unit tests for domain error hierarchy."""

from packages.core.errors import (
    ApprovalRequired,
    CofunderError,
    PolicyViolation,
    TenantIsolationError,
    ValidationError,
)


def test_cofunder_error_inheritance() -> None:
    """Verify that domain exceptions correctly inherit from CofunderError."""
    assert issubclass(ValidationError, CofunderError)
    assert issubclass(PolicyViolation, CofunderError)
    assert issubclass(TenantIsolationError, PolicyViolation)
    assert issubclass(ApprovalRequired, CofunderError)


def test_approval_required_details() -> None:
    """Verify ApprovalRequired captures tool name and argument metadata."""
    err = ApprovalRequired(tool_name="publish_post", action_args={"platform": "x", "text": "launch!"})
    assert err.tool_name == "publish_post"
    assert err.action_args["platform"] == "x"
    assert "publish_post" in str(err)
    assert err.details["tool_name"] == "publish_post"
