"""Approval service interface and logic for human-in-the-loop gating."""

import hashlib
import json
from typing import Any, Protocol
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from packages.core.context import AgentContext
from packages.decisions.policy.hard_rules import is_never_auto


def _compute_grant_key(
    tenant_id: str,
    venture_id: str,
    action: str,
    args: Any,
) -> tuple[str, str, str, str]:
    """Compute a deterministic hash key for an approved action payload."""
    payload_str = ""
    if isinstance(args, BaseModel):
        payload_str = args.model_dump_json()
    elif isinstance(args, dict):
        try:
            payload_str = json.dumps(args, sort_keys=True)
        except Exception:
            payload_str = str(sorted(args.items()))
    elif args is not None:
        payload_str = str(args)
    payload_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    return (tenant_id, venture_id, action, payload_hash)


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
        self.granted_actions: set[tuple[str, str, str, str]] = set()

    def set_auto_approval(self, action: str, allowed: bool) -> None:
        """Configure auto-approval policy for an action type.

        Payments, legal documents, and filings can NEVER be auto-approved.

        Args:
            action: The tool or action name.
            allowed: True if auto-approved, False otherwise.
        """
        if is_never_auto(action):
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
        grant_key = _compute_grant_key(req.tenant_id, req.venture_id, req.action, req.payload)
        if status == "approved":
            self.granted_actions.add(grant_key)
        elif status == "rejected":
            self.granted_actions.discard(grant_key)
        return True

    async def is_approved(
        self,
        ctx: AgentContext,
        action: str,
        args: Any,
    ) -> bool:
        """Check if action is pre-granted or auto-approved."""
        grant_key = _compute_grant_key(ctx.tenant_id, ctx.venture_id, action, args)

        # 1. Hard-coded blocks on payments, legal, filings
        if is_never_auto(action):
            return grant_key in self.granted_actions

        # 2. Check auto-approval policy
        if self.auto_approval_policies.get(action, False):
            return True

        # 3. Check explicit approval grant
        return grant_key in self.granted_actions
