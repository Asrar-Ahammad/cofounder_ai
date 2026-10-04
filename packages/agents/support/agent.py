"""Support and Reception Agent LangGraph subgraph builder."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.support.answer_grounded import answer_from_approved_knowledge
from packages.agents.support.detect_sentiment import evaluate_customer_sentiment
from packages.agents.support.escalate_ticket import escalate_to_founder
from packages.agents.support.format_reply import format_customer_response
from packages.agents.support.route_intent import route_customer_intent
from packages.agents.support.state import SupportState


class SupportAgent:
    """Specialist agent handling 24/7 inbound inquiries, sentiment triage, and KB Q&A."""

    name: str = "support_agent"
    allowed_tools: frozenset[str] = frozenset({"send_chat_message", "book_calendar_meeting"})
    consumes: frozenset[str] = frozenset({"customer_inquiry_received", "webhook_message_enqueued"})
    emits: frozenset[str] = frozenset({"support_responded", "support_escalated"})

    def build_graph(self) -> Any:
        """Construct and compile the Support Agent LangGraph subgraph.

        Returns:
            CompiledStateGraph: Executable support pipeline.
        """
        builder = StateGraph(SupportState)
        builder.add_node("detect_sentiment", evaluate_customer_sentiment)
        builder.add_node("route_intent", route_customer_intent)
        builder.add_node("answer_grounded", answer_from_approved_knowledge)
        builder.add_node("escalate_founder", escalate_to_founder)
        builder.add_node("format_reply", format_customer_response)

        def route_after_sentiment(state: SupportState) -> str:
            if state.frustration_level in ("frustrated", "urgent_risk"):
                return "escalate_founder"
            return "route_intent"

        def route_after_intent(state: SupportState) -> str:
            if state.routing_decision == "spam":
                return "end"
            if state.routing_decision == "escalate":
                return "escalate_founder"
            if state.routing_decision == "book_meeting":
                return "format_reply"
            return "answer_grounded"

        def route_after_grounding(state: SupportState) -> str:
            if state.requires_escalation:
                return "escalate_founder"
            return "format_reply"

        builder.add_edge(START, "detect_sentiment")
        builder.add_conditional_edges(
            "detect_sentiment",
            route_after_sentiment,
            {"escalate_founder": "escalate_founder", "route_intent": "route_intent"},
        )
        builder.add_conditional_edges(
            "route_intent",
            route_after_intent,
            {
                "end": END,
                "escalate_founder": "escalate_founder",
                "format_reply": "format_reply",
                "answer_grounded": "answer_grounded",
            },
        )
        builder.add_conditional_edges(
            "answer_grounded",
            route_after_grounding,
            {"escalate_founder": "escalate_founder", "format_reply": "format_reply"},
        )
        builder.add_edge("escalate_founder", END)
        builder.add_edge("format_reply", END)

        return builder.compile()
