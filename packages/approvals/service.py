"""Approval service interface and logic for human-in-the-loop gating."""

from typing import Any, Protocol
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.core.context import AgentContext


class ApprovalRequest(BaseModel):
    """Model representing an approval record."""

    id: UUID = Field(default_factory=uuid4)
    tenant_id: str
    venture_id: str
    action: str
    payload: dict[str, Any]
    risk_level: str = "medium"
    status: str = "pending"  # pending, approved, rejected, auto_approved
    resolved_by: str | None = None


class ApprovalService(Protocol):
    """Protocol for managing and evaluating human approval states."""

    async def is_approved(
        self,
        ctx: AgentContext,
        action: str,
        args: Any,
    ) -> bool:
        """Check whether human approval has already been granted for this action.

        Args:
            ctx: Current agent execution context.
            action: Name of the gated tool or operation.
            args: Validated arguments model or dict.

        Returns:
            bool: True if approved or auto-approved by policy, False otherwise.
        """
        ...


class InMemoryApprovalService:
    """In-memory approval service managing pending approvals and policies."""

    def __init__(self) -> None:
        """Initialize empty approval service."""
        self.requests: dict[UUID, ApprovalRequest] = {}
        self.auto_approval_policies: dict[str, bool] = {}
        self.granted_actions: set[tuple[str, str, str]] = set()

    def set_auto_approval(self, action: str, allowed: bool) -> None:
        """Configure auto-approval policy for an action type.

        Payments, legal documents, and filings can NEVER be auto-approved.

        Args:
            action: The tool or action name.
            allowed: True if auto-approved, False otherwise.
        """
        if action in ("send_payment", "file_regulatory", "sign_legal"):
            self.auto_approval_policies[action] = False
            return
        self.auto_approval_policies[action] = allowed

    async def create_request(
        self,
        ctx: AgentContext,
        action: str,
        payload: dict[str, Any],
        risk_level: str = "medium",
    ) -> ApprovalRequest:
        """Create and store a pending approval request."""
        req = ApprovalRequest(
            tenant_id=ctx.tenant_id,
            venture_id=ctx.venture_id,
            action=action,
            payload=payload,
            risk_level=risk_level,
        )
        self.requests[req.id] = req
        return req

    async def resolve_request(
        self,
        request_id: UUID,
        status: str,
        resolved_by: str,
    ) -> bool:
        """Resolve a pending approval request."""
        req = self.requests.get(request_id)
        if not req:
            return False

        req.status = status
        req.resolved_by = resolved_by
        if status == "approved":
            # Grant for (tenant_id, venture_id, action)
            self.granted_actions.add((req.tenant_id, req.venture_id, req.action))
        return True

    async def is_approved(
        self,
        ctx: AgentContext,
        action: str,
        _args: Any,
    ) -> bool:
        """Check if action is pre-granted or auto-approved."""
        # 1. Hard-coded blocks on payments and filings
        if action in ("send_payment", "file_regulatory", "sign_legal"):
            return (ctx.tenant_id, ctx.venture_id, action) in self.granted_actions

        # 2. Check auto-approval policy
        if self.auto_approval_policies.get(action, False):
            return True

        # 3. Check explicit approval grant
        return (ctx.tenant_id, ctx.venture_id, action) in self.granted_actions
