"""Unit tests for Sales Agent, immediate suppression, and crisis triage."""

import pytest
from pydantic import BaseModel

from packages.agents.sales.agent import SalesAgent
from packages.agents.sales.draft_outreach_email import draft_personalized_outreach
from packages.agents.sales.process_reply import process_inbound_outreach_reply
from packages.agents.sales.qualify_prospect import qualify_sales_prospect
from packages.agents.sales.state import SalesState
from packages.agents.sales.triage_inbound_message import triage_inbound_interaction
from packages.approvals.service import ApprovalService
from packages.core.context import AgentContext, AgentInfo
from packages.core.errors import PolicyViolation
from packages.core.suppression import clear_suppression_list, is_email_suppressed
from packages.tools.gateway import ToolGateway
from packages.tools.registry import ToolRegistry, ToolSpec


class EmailArgs(BaseModel):
    recipient: str
    subject: str


def test_sales_agent_qualification_and_outreach() -> None:
    """Verify high-intent prospect is qualified for call and outreach is staged."""
    clear_suppression_list("t1")
    state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        prospect_profile="CTO at Seed-stage Developer Infrastructure startup",
        prospect_email="alex@devinfra.io",
    )

    state = qualify_sales_prospect(state)
    assert state.qualification_status == "book_call"

    state = draft_personalized_outreach(state)
    assert "alex@devinfra.io" in state.summary
    assert "15-minute introductory conversation" in state.outreach_draft
    assert state.needs_approval is True


def test_sales_agent_immediate_unsubscribe_suppression() -> None:
    """Verify unsubscribe reply triggers immediate suppression at code level."""
    clear_suppression_list("t1")
    email = "prospect@optout.com"

    state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        prospect_email=email,
        reply_text="Please stop emailing me. Unsubscribe immediately.",
    )

    assert is_email_suppressed("t1", email) is False

    state = process_inbound_outreach_reply(state)
    assert state.reply_classification == "unsubscribe"
    assert state.is_suppressed is True
    assert is_email_suppressed("t1", email) is True

    # Subsequent outreach to the same recipient is blocked
    new_state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        prospect_profile="CTO at Cloud Co",
        prospect_email=email,
        qualification_status="book_call",
    )
    new_state = draft_personalized_outreach(new_state)
    assert new_state.is_suppressed is True
    assert new_state.outreach_draft == ""
    assert "Outreach blocked" in new_state.summary


@pytest.mark.asyncio
async def test_tool_gateway_blocks_suppressed_email() -> None:
    """Verify ToolGateway throws PolicyViolation when target email is suppressed."""
    clear_suppression_list("tenant-gate")
    email = "suppressed@domain.com"
    from packages.core.suppression import add_to_suppression_list
    add_to_suppression_list("tenant-gate", email, reason="unsubscribe")

    registry = ToolRegistry()

    async def mock_send(tenant_id: str, args: EmailArgs, idempotency_key: str) -> str:
        return "sent"

    registry.register(
        ToolSpec(
            name="send_email",
            description="Send an email",
            args_model=EmailArgs,
            adapter_fn=mock_send,
            requires_approval=False,
        )
    )

    class MockApprovalService(ApprovalService):
        async def is_approved(self, ctx: AgentContext, tool_name: str, args: BaseModel) -> bool:
            return True

    gateway = ToolGateway(approval_service=MockApprovalService(), registry=registry)
    ctx = AgentContext(
        tenant_id="tenant-gate",
        venture_id="v1",
        run_id="run_123",
        agent=AgentInfo(name="sales_agent", allowed_tools=frozenset({"send_email"})),
    )

    with pytest.raises(PolicyViolation, match="on the suppression list"):
        await gateway.execute_tool(ctx, "send_email", {"recipient": email, "subject": "Test"})


def test_sales_agent_crisis_triage() -> None:
    """Verify crisis comment halts automation and triggers founder alert."""
    state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        inbound_type="comment",
        reply_text="Your service leaked our confidential database! We are taking legal action with our lawyer.",
    )

    state = triage_inbound_interaction(state)
    assert state.triage_category == "crisis"
    assert state.crisis_alert_sent is True
    assert "CRISIS ALERT" in state.summary


@pytest.mark.asyncio
async def test_sales_agent_graph_execution() -> None:
    """Verify Sales Agent compiled LangGraph executes end-to-end for lead qualification."""
    clear_suppression_list("t1")
    agent = SalesAgent()
    graph = agent.build_graph()

    state = SalesState(
        tenant_id="t1",
        venture_id="v1",
        prospect_profile="Head of Engineering at Seed AI company",
        prospect_email="eng@ai-seed.io",
    )

    final = await graph.ainvoke(state)
    assert final["qualification_status"] == "book_call"
    assert "eng@ai-seed.io" in final["summary"]
    assert len(final["outreach_draft"]) > 0
