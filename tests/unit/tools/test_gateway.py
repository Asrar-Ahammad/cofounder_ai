"""Unit tests for ToolGateway security controls, allowlists, and approvals."""

from typing import Any

import pytest
from pydantic import BaseModel, Field

from packages.core.context import AgentContext, AgentInfo
from packages.core.errors import ApprovalRequired, PolicyViolation
from packages.tools.gateway import ToolGateway
from packages.tools.registry import ToolRegistry, ToolSpec


class DummyPostArgs(BaseModel):
    """Test schema for post tool arguments."""

    platform: str
    text: str = Field(..., max_length=100)


class MockApprovalService:
    """Mock approval service for testing."""

    def __init__(self, should_approve: bool = False) -> None:
        """Initialize mock approval service."""
        self.should_approve = should_approve

    async def is_approved(self, ctx: AgentContext, action: str, args: Any) -> bool:
        """Return preset approval status."""
        return self.should_approve


@pytest.mark.asyncio
async def test_tool_gateway_rejects_unauthorized_tool() -> None:
    """Verify ToolGateway blocks tools not present in agent allowed_tools."""
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="send_payment",
            description="Send payment",
            args_model=DummyPostArgs,
            adapter_fn=lambda *a, **kw: "ok",
        )
    )
    gateway = ToolGateway(approval_service=MockApprovalService(), registry=registry)

    ctx = AgentContext(
        tenant_id="tenant-1",
        venture_id="venture-1",
        run_id="run-1",
        agent=AgentInfo(name="receptionist", allowed_tools=frozenset(["answer_faq"])),
    )

    with pytest.raises(PolicyViolation, match="unauthorized"):
        await gateway.execute_tool(ctx, "send_payment", {"platform": "stripe", "text": "pay"})


@pytest.mark.asyncio
async def test_tool_gateway_requires_approval() -> None:
    """Verify ToolGateway raises ApprovalRequired when unapproved."""
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="publish_post",
            description="Publish post",
            args_model=DummyPostArgs,
            adapter_fn=lambda *a, **kw: "published-123",
            requires_approval=True,
        )
    )
    gateway = ToolGateway(approval_service=MockApprovalService(should_approve=False), registry=registry)

    ctx = AgentContext(
        tenant_id="tenant-1",
        venture_id="venture-1",
        run_id="run-1",
        agent=AgentInfo(name="social_agent", allowed_tools=frozenset(["publish_post"])),
    )

    with pytest.raises(ApprovalRequired):
        await gateway.execute_tool(ctx, "publish_post", {"platform": "x", "text": "Hello world!"})


@pytest.mark.asyncio
async def test_tool_gateway_executes_and_caches_idempotency() -> None:
    """Verify ToolGateway executes approved action and returns cached result on replay."""
    call_count = 0

    async def mock_adapter(tenant_id: str, args: DummyPostArgs, idempotency_key: str) -> str:
        nonlocal call_count
        call_count += 1
        return f"result-{args.text}"

    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="publish_post",
            description="Publish post",
            args_model=DummyPostArgs,
            adapter_fn=mock_adapter,
            requires_approval=True,
        )
    )
    gateway = ToolGateway(approval_service=MockApprovalService(should_approve=True), registry=registry)

    ctx = AgentContext(
        tenant_id="tenant-1",
        venture_id="venture-1",
        run_id="run-1",
        agent=AgentInfo(name="social_agent", allowed_tools=frozenset(["publish_post"])),
    )

    res1 = await gateway.execute_tool(ctx, "publish_post", {"platform": "x", "text": "Replay test"})
    assert res1 == "result-Replay test"
    assert call_count == 1

    # Second execution with identical arguments in same run should hit idempotency cache
    res2 = await gateway.execute_tool(ctx, "publish_post", {"platform": "x", "text": "Replay test"})
    assert res2 == "result-Replay test"
    assert call_count == 1


def test_tool_registry_rejects_duplicate_registration() -> None:
    """Verify ToolRegistry raises ValueError when registering a duplicate tool name."""
    registry = ToolRegistry()
    spec = ToolSpec(
        name="test_tool",
        description="Test",
        args_model=DummyPostArgs,
        adapter_fn=lambda *a, **kw: None,
    )
    registry.register(spec)
    with pytest.raises(ValueError, match="already registered"):
        registry.register(spec)
