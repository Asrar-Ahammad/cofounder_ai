"""Core domain exception hierarchy for Cofunder.

All internal errors inherit from CofunderError to ensure controlled exception
mapping at API and tool boundaries.
"""

from typing import Any


class CofunderError(Exception):
    """Base exception for all domain errors in Cofunder."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize domain error with message and optional context details.

        Args:
            message: Human-readable error message.
            details: Optional dictionary containing error metadata.
        """
        super().__init__(message)
        self.message = message
        self.details = details or {}


class ValidationError(CofunderError):
    """Raised when data or argument fails schema or semantic validation."""


class PolicyViolation(CofunderError):
    """Raised when an operation violates security, tenancy, or financial constraints."""


class ApprovalRequired(CofunderError):
    """Raised when a tool or action cannot proceed without human confirmation."""

    def __init__(self, tool_name: str, action_args: dict[str, Any]) -> None:
        """Initialize approval required exception.

        Args:
            tool_name: The name of the gated tool.
            action_args: The arguments passed to the gated tool.
        """
        super().__init__(
            f"Action '{tool_name}' requires human approval",
            details={"tool_name": tool_name, "args": action_args},
        )
        self.tool_name = tool_name
        self.action_args = action_args


class ExternalServiceError(CofunderError):
    """Raised when an external third-party adapter call fails."""


class TenantIsolationError(PolicyViolation):
    """Raised when an operation attempts unauthorized cross-tenant data access."""
