"""Sales Agent LangGraph subgraph builder."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.sales.draft_outreach_email import draft_personalized_outreach
from packages.agents.sales.process_reply import process_inbound_outreach_reply
from packages.agents.sales.qualify_prospect import qualify_sales_prospect
from packages.agents.sales.state import SalesState
from packages.agents.sales.triage_inbound_message import triage_inbound_interaction


class SalesAgent:
    """Specialist agent qualifying leads, drafting outreach, and triaging replies."""

    name: str = "sales_agent"
    allowed_tools: frozenset[str] = frozenset({"send_outreach_email", "book_calendar_meeting"})
    consumes: frozenset[str] = frozenset({"lead_discovered", "reply_received", "inbound_message_received"})
    emits: frozenset[str] = frozenset({"outreach_drafted", "lead_suppressed", "crisis_alerted"})

    def build_graph(self) -> Any:
        """Construct and compile the Sales Agent LangGraph subgraph.

        Returns:
            CompiledStateGraph: Executable sales pipeline.
        """
        builder = StateGraph(SalesState)
        builder.add_node("qualify_lead", qualify_sales_prospect)
        builder.add_node("draft_outreach", draft_personalized_outreach)
        builder.add_node("process_reply", process_inbound_outreach_reply)
        builder.add_node("triage_inbound", triage_inbound_interaction)

        def route_by_inbound_type(state: SalesState) -> str:
            if state.inbound_type in ("comment", "dm"):
                return "triage_inbound"
            if state.reply_text:
                return "process_reply"
            return "qualify_lead"

        builder.add_conditional_edges(
            START,
            route_by_inbound_type,
            {
                "triage_inbound": "triage_inbound",
                "process_reply": "process_reply",
                "qualify_lead": "qualify_lead",
            },
        )
        builder.add_edge("qualify_lead", "draft_outreach")
        builder.add_edge("draft_outreach", END)
        builder.add_edge("process_reply", END)
        builder.add_edge("triage_inbound", END)

        return builder.compile()
