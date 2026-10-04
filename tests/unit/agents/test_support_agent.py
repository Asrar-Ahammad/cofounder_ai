"""Unit tests for Support and Reception Agent and sentiment-guided routing."""

import pytest

from packages.agents.support.agent import SupportAgent
from packages.agents.support.answer_grounded import answer_from_approved_knowledge
from packages.agents.support.detect_sentiment import evaluate_customer_sentiment
from packages.agents.support.escalate_ticket import escalate_to_founder
from packages.agents.support.format_reply import format_customer_response
from packages.agents.support.route_intent import route_customer_intent
from packages.agents.support.state import SupportState


def test_support_sentiment_detection_calm_and_frustrated() -> None:
    """Verify customer sentiment accurately detects calm, frustrated, and urgent risk."""
    state_calm = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_001",
        incoming_message="Hello, where can I find the API documentation?",
    )
    state_calm = evaluate_customer_sentiment(state_calm)
    assert state_calm.frustration_level == "calm"
    assert state_calm.requires_escalation is False

    state_frustrated = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_002",
        incoming_message="This feature is broken and completely useless, terrible experience!",
    )
    state_frustrated = evaluate_customer_sentiment(state_frustrated)
    assert state_frustrated.frustration_level == "frustrated"
    assert state_frustrated.requires_escalation is True

    state_urgent = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_003",
        incoming_message="There is a critical security breach and our lawyer is filing a lawsuit!",
    )
    state_urgent = evaluate_customer_sentiment(state_urgent)
    assert state_urgent.frustration_level == "urgent_risk"
    assert state_urgent.requires_escalation is True


def test_support_intent_routing() -> None:
    """Verify intent router classifies meetings, spam, enterprise escalations, and Q&A."""
    state_demo = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_004",
        incoming_message="I would like to schedule a demo call with the founder.",
    )
    state_demo = route_customer_intent(state_demo)
    assert state_demo.routing_decision == "book_meeting"
    assert state_demo.booking_link is not None

    state_spam = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_005",
        incoming_message="Check our bio for crypto airdrop and follow back!",
    )
    state_spam = route_customer_intent(state_spam)
    assert state_spam.routing_decision == "spam"

    state_pricing = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_006",
        incoming_message="What are your standard pricing tiers?",
    )
    state_pricing = route_customer_intent(state_pricing)
    assert state_pricing.routing_decision == "answer_from_kb"


def test_grounded_kb_answer_and_abstention() -> None:
    """Verify KB answer cites sources and abstains from ungrounded claims."""
    state_known = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_007",
        incoming_message="What is your pricing policy?",
    )
    state_known = answer_from_approved_knowledge(state_known)
    assert "starter tier is $29/month" in state_known.kb_answer
    assert "kb:pricing" in state_known.citations
    assert state_known.requires_escalation is False

    # Ungrounded topic triggers abstention
    state_unknown = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_008",
        incoming_message="Do you provide on-premise hardware mainframes in Antarctica?",
    )
    state_unknown = answer_from_approved_knowledge(state_unknown)
    assert state_unknown.requires_escalation is True
    assert "absent from approved knowledge base" in (state_unknown.escalation_reason or "")


@pytest.mark.asyncio
async def test_support_agent_graph_execution_calm_kb() -> None:
    """Verify Support Agent compiled graph answers calm inquiries from knowledge base."""
    agent = SupportAgent()
    graph = agent.build_graph()

    state = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="user_whatsapp_101",
        channel="whatsapp",
        incoming_message="Can you tell me about your security and encryption standards?",
    )

    final = await graph.ainvoke(state)
    assert final["frustration_level"] == "calm"
    assert final["routing_decision"] == "answer_from_kb"
    assert "AES-256" in final["response_text"]
    assert "kb:security" in final["citations"]
    assert final["requires_escalation"] is False


@pytest.mark.asyncio
async def test_support_agent_graph_execution_frustration_escalation() -> None:
    """Verify Support Agent compiled graph immediately escalates frustrated queries."""
    agent = SupportAgent()
    graph = agent.build_graph()

    state = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="user_web_202",
        channel="web",
        incoming_message="Your platform is completely broken, awful customer experience!",
    )

    final = await graph.ainvoke(state)
    assert final["frustration_level"] == "frustrated"
    assert final["requires_escalation"] is True
    assert "escalated your request to our founder" in final["response_text"]


def test_support_escalate_and_format_nodes() -> None:
    """Verify escalate_to_founder and format_customer_response individual functions."""
    state_esc = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_esc",
        incoming_message="Need immediate founder discussion.",
        escalation_reason="Executive contract negotiation.",
    )
    state_esc = escalate_to_founder(state_esc)
    assert state_esc.requires_escalation is True
    assert "escalated your request to our founder" in state_esc.response_text

    state_format = SupportState(
        tenant_id="t1",
        venture_id="v1",
        customer_id="cust_fmt",
        incoming_message="What is the setup time?",
        routing_decision="answer_from_kb",
        kb_answer="Setup takes 5 minutes.",
        citations=["kb:setup"],
    )
    state_format = format_customer_response(state_format)
    assert "Setup takes 5 minutes." in state_format.response_text
    assert "[Ref: kb:setup]" in state_format.response_text

