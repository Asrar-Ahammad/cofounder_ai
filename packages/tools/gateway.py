"""Tool Gateway: Single choke-point for all external side effects and tool executions."""

import hashlib
import json
from collections import OrderedDict
from typing import Any

from packages.approvals.service import ApprovalService
from packages.core.context import AgentContext
from packages.core.errors import ApprovalRequired, PolicyViolation
from packages.core.suppression import is_email_suppressed
from packages.tools.registry import ToolRegistry, tool_registry

MAX_IDEMPOTENCY_CACHE_SIZE = 1000


class ToolGateway:
    """Central gateway enforcing security, schemas, approvals, and idempotency."""

    def __init__(
        self,
        approval_service: ApprovalService,
        registry: ToolRegistry = tool_registry,
    ) -> None:
        """Initialize Tool Gateway with dependencies.

        Args:
            approval_service: Service evaluating human-in-the-loop approvals.
            registry: Tool registry containing available ToolSpecs.
        """
        self.approval_service = approval_service
        self.registry = registry
        self._idempotency_cache: OrderedDict[str, Any] = OrderedDict()

    def compute_idempotency_key(self, run_id: str, tool_name: str, args: dict[str, Any]) -> str:
        """Calculate deterministic SHA256 idempotency key for this call.

        Args:
            run_id: Active agent execution run ID.
            tool_name: Unique name of the tool.
            args: Serialized dictionary of tool arguments.

        Returns:
            str: 64-character hex hash.
        """
        serialized = json.dumps(args, sort_keys=True)
        raw = f"{run_id}:{tool_name}:{serialized}".encode()
        return hashlib.sha256(raw).hexdigest()

    async def execute_tool(
        self,
        ctx: AgentContext,
        name: str,
        raw_args: dict[str, Any],
    ) -> Any:
        """Execute a tool through the secure gateway choke-point.

        Args:
            ctx: Execution context of the calling agent.
            name: Target tool name.
            raw_args: Untrusted argument dictionary.

        Returns:
            Any: Result of the tool execution.

        Raises:
            PolicyViolation: If tool is unknown, agent unauthorized, or constraints fail.
            ApprovalRequired: If tool requires human confirmation.
        """
        spec = self.registry.get(name)
        if not spec:
            raise PolicyViolation(f"Unknown tool: '{name}'")

        if name not in ctx.agent.allowed_tools:
            raise PolicyViolation(f"Agent '{ctx.agent.name}' is unauthorized to call tool '{name}'")

        validated_args = spec.args_model.model_validate(raw_args)

        recipient = getattr(validated_args, "recipient", None) or getattr(validated_args, "recipient_email", None)
        if recipient and is_email_suppressed(ctx.tenant_id, str(recipient)):
            raise PolicyViolation(f"Recipient '{recipient}' is on the suppression list. Outbound communication blocked.")

        if spec.policy_check:
            spec.policy_check(ctx.tenant_id, ctx.venture_id, validated_args)

        if spec.requires_approval:
            is_approved = await self.approval_service.is_approved(ctx, name, validated_args)
            if not is_approved:
                raise ApprovalRequired(tool_name=name, action_args=validated_args.model_dump())

        key = self.compute_idempotency_key(ctx.run_id, name, validated_args.model_dump())
        if key in self._idempotency_cache:
            self._idempotency_cache.move_to_end(key)
            return self._idempotency_cache[key]

        result = await spec.adapter_fn(ctx.tenant_id, validated_args, idempotency_key=key)
        self._idempotency_cache[key] = result
        if len(self._idempotency_cache) > MAX_IDEMPOTENCY_CACHE_SIZE:
            self._idempotency_cache.popitem(last=False)
        return result
