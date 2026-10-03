"""Legal and Regulatory Agent subgraph implementation."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.legal.evaluate_regulatory_gate import evaluate_statutory_grounding
from packages.agents.legal.retrieve_statutes import retrieve_relevant_statutes
from packages.agents.legal.state import LegalState
from packages.agents.legal.synthesize_legal_memo import synthesize_legal_memorandum


class LegalAgent:
    """Specialist agent for statutory compliance, regulatory RAG, and mandatory citation gating."""

    name: str = "legal_agent"
    allowed_tools: frozenset[str] = frozenset()
    consumes: frozenset[str] = frozenset({"regulatory_risk_flagged", "venture_incorporation_requested"})
    emits: frozenset[str] = frozenset({"legal_memo_generated", "legal_counsel_required"})

    def build_graph(self) -> Any:
        """Construct and compile the Legal Agent LangGraph subgraph.

        Returns:
            CompiledStateGraph: Executable legal RAG subgraph.
        """
        builder = StateGraph(LegalState)
        builder.add_node("retrieve_statutes", retrieve_relevant_statutes)
        builder.add_node("evaluate_gate", evaluate_statutory_grounding)
        builder.add_node("synthesize_memo", synthesize_legal_memorandum)

        builder.add_edge(START, "retrieve_statutes")
        builder.add_edge("retrieve_statutes", "evaluate_gate")
        builder.add_edge("evaluate_gate", "synthesize_memo")
        builder.add_edge("synthesize_memo", END)

        return builder.compile()
