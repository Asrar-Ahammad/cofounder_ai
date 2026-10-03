"""Integration test verifying LangGraph interrupt() and resumption with ApprovalService."""

from typing import Any

import pytest
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.types import Command, interrupt

from packages.approvals.service import InMemoryApprovalService
from packages.core.context import AgentContext, AgentInfo


class WorkflowState(dict[str, Any]):
    """Typed state for test workflow."""
    status: str
    action_result: str


@pytest.mark.asyncio
async def test_langgraph_interrupt_and_resume_flow() -> None:
    """Verify workflow pauses on interrupt and resumes with human approval Command."""
    approval_svc = InMemoryApprovalService()
    ctx = AgentContext(
        tenant_id="tenant-123",
        venture_id="venture-456",
        run_id="run-789",
        agent=AgentInfo(name="marketing_agent", allowed_tools=frozenset(["publish_post"])),
    )

    async def draft_post_node(state: WorkflowState) -> dict[str, Any]:
        return {"status": "drafted"}

    async def publish_node(state: WorkflowState) -> dict[str, Any]:
        is_approved = await approval_svc.is_approved(ctx, "publish_post", {"content": "Launch day!"})
        if not is_approved:
            # Create pending approval request and pause graph
            req = await approval_svc.create_request(ctx, "publish_post", {"content": "Launch day!"})
            decision = interrupt({"request_id": str(req.id), "action": "publish_post"})
            if decision != "approved":
                return {"status": "rejected", "action_result": "aborted"}

        return {"status": "published", "action_result": "post-id-999"}

    builder = StateGraph(WorkflowState)
    builder.add_node("draft_post", draft_post_node)
    builder.add_node("publish", publish_node)
    builder.add_edge(START, "draft_post")
    builder.add_edge("draft_post", "publish")

    checkpointer = MemorySaver()
    graph = builder.compile(checkpointer=checkpointer)

    thread_config = {"configurable": {"thread_id": "thread-1"}}

    # First invocation should pause at publish_node with interrupt
    events = []
    async for event in graph.astream({"status": "starting", "action_result": ""}, thread_config):
        events.append(event)

    # Verify run is paused waiting for approval
    snapshot = await graph.aget_state(thread_config)
    assert snapshot.next == ("publish",)
    assert len(approval_svc.requests) == 1
    req = list(approval_svc.requests.values())[0]
    assert req.status == "pending"

    # Human approves the request
    await approval_svc.resolve_request(req.id, status="approved", resolved_by="founder@test.com")

    # Resume the graph with Command(resume="approved")
    resume_events = []
    async for event in graph.astream(Command(resume="approved"), thread_config):
        resume_events.append(event)

    final_snapshot = await graph.aget_state(thread_config)
    assert final_snapshot.values["status"] == "published"
    assert final_snapshot.values["action_result"] == "post-id-999"


@pytest.mark.asyncio
async def test_approval_service_payload_isolation_and_rejection() -> None:
    """Verify approval is payload-specific and revoked on rejection."""
    approval_svc = InMemoryApprovalService()
    ctx = AgentContext(
        tenant_id="tenant-1",
        venture_id="venture-1",
        run_id="run-1",
        agent=AgentInfo(name="finance_agent", allowed_tools=frozenset(["send_payment"])),
    )
    req = await approval_svc.create_request(ctx, "send_payment", {"amount": 100, "to": "Alice"})
    assert not await approval_svc.is_approved(ctx, "send_payment", {"amount": 100, "to": "Alice"})

    await approval_svc.resolve_request(req.id, "approved", "founder@test.com")
    # Exact payload is now approved
    assert await approval_svc.is_approved(ctx, "send_payment", {"amount": 100, "to": "Alice"})
    # Different payload for same action is NOT approved
    assert not await approval_svc.is_approved(ctx, "send_payment", {"amount": 200, "to": "Bob"})

    # Rejecting revokes approval
    await approval_svc.resolve_request(req.id, "rejected", "founder@test.com")
    assert not await approval_svc.is_approved(ctx, "send_payment", {"amount": 100, "to": "Alice"})
