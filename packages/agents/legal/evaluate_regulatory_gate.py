"""Regulatory gate node applying Decision D11 to enforce mandatory citation or abstention."""

from packages.agents.legal.state import LegalState
from packages.decisions.definitions.gate_legal_answer import fail_closed_gate_legal_answer


def evaluate_statutory_grounding(state: LegalState) -> LegalState:
    """Evaluate retrieval confidence to determine whether to answer or strictly abstain.

    Args:
        state: Active Legal agent state.

    Returns:
        LegalState: State updated with the answer or abstain decision.
    """
    if not state.retrieved_chunks:
        state.decision = fail_closed_gate_legal_answer()
        state.requires_human_counsel = True
        return state

    top_score = float(state.retrieved_chunks[0].get("score", 0.0))
    # Threshold for grounded answer: minimum 0.25 relevance to prevent ungrounded claims
    if top_score >= 0.25:
        state.decision = "answer"
        state.requires_human_counsel = False
    else:
        state.decision = "abstain"
        state.requires_human_counsel = True

    return state
