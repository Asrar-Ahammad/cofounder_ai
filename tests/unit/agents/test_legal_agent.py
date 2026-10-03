"""Unit tests for Legal and Regulatory Agent subgraph and abstention gates."""

import pytest

from packages.agents.legal.agent import LegalAgent
from packages.agents.legal.evaluate_regulatory_gate import evaluate_statutory_grounding
from packages.agents.legal.retrieve_statutes import retrieve_relevant_statutes
from packages.agents.legal.state import LegalState
from packages.agents.legal.synthesize_legal_memo import synthesize_legal_memorandum


def test_legal_agent_grounded_answer_flow() -> None:
    """Verify grounded statutory retrieval produces cited memorandum when matched."""
    state = LegalState(
        tenant_id="t1",
        venture_id="v1",
        jurisdiction="IN",
        query="notice and consent obligations for processing personal data",
    )

    state = retrieve_relevant_statutes(state)
    assert len(state.retrieved_chunks) > 0
    assert len(state.citation_refs) > 0
    assert any("DPDP" in c or "Digital Personal Data" in c for c in state.citation_refs)

    state = evaluate_statutory_grounding(state)
    assert state.decision == "answer"
    assert state.requires_human_counsel is False

    state = synthesize_legal_memorandum(state)
    assert "Section" in state.analysis
    assert "Disclaimer" in state.analysis
    assert "Digital Personal Data" in state.analysis
    assert "Synthesized grounded statutory memorandum" in state.summary


def test_legal_agent_mandatory_abstention_on_out_of_corpus_query() -> None:
    """Verify mandatory abstention when no verified statutory provisions match query."""
    state = LegalState(
        tenant_id="t1",
        venture_id="v1",
        jurisdiction="IN",
        query="deep sea mining mineral rights in antarctica",
    )

    state = retrieve_relevant_statutes(state)
    assert len(state.retrieved_chunks) == 0

    state = evaluate_statutory_grounding(state)
    assert state.decision == "abstain"
    assert state.requires_human_counsel is True

    state = synthesize_legal_memorandum(state)
    assert "ABSTENTION:" in state.analysis
    assert "strictly abstains" in state.analysis
    assert "licensed attorney" in state.analysis
    assert "strictly abstained" in state.summary


@pytest.mark.asyncio
async def test_legal_agent_graph_execution() -> None:
    """Verify Legal Agent compiled LangGraph executes end-to-end."""
    agent = LegalAgent()
    graph = agent.build_graph()

    state = LegalState(
        tenant_id="t1",
        venture_id="v1",
        jurisdiction="US-DE",
        query="incorporators certificate of incorporation requirements",
    )

    final_state = await graph.ainvoke(state)
    assert final_state["decision"] == "answer"
    assert len(final_state["citation_refs"]) >= 1
    assert "Delaware" in final_state["analysis"]
