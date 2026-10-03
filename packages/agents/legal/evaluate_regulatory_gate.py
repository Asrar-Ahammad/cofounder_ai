"""Regulatory gate node applying Decision D11 to enforce mandatory citation, clarification, or abstention."""

from packages.agents.legal.state import LegalState
from packages.decisions.definitions.gate_legal_answer import fail_closed_gate_legal_answer


def evaluate_statutory_grounding(state: LegalState) -> LegalState:
    """Evaluate retrieval grounding and citation validity to answer, clarify, or abstain.

    Args:
        state: Active Legal agent state.

    Returns:
        LegalState: State updated with the decision and counsel requirement.
    """
    if not state.retrieved_chunks:
        state.decision = fail_closed_gate_legal_answer()
        state.requires_human_counsel = True
        return state

    top = state.retrieved_chunks[0]
    source_url = str(top.get("source_url", ""))
    sec_num = str(top.get("section_number", "")) or str(top.get("citation", ""))
    top_score = float(top.get("score", 0.0))

    # Citation grounding validation: must link to official HTTPS gazette and valid section
    has_valid_citation = source_url.startswith("https://") and len(sec_num) > 0
    if not has_valid_citation:
        state.decision = fail_closed_gate_legal_answer()
        state.requires_human_counsel = True
        return state

    # Ambiguity and confidence threshold evaluation
    if top_score >= 0.35:
        state.decision = "answer"
        state.requires_human_counsel = False
    elif top_score >= 0.20:
        state.decision = "clarify"
        state.requires_human_counsel = False
    else:
        state.decision = "abstain"
        state.requires_human_counsel = True

    return state
