"""Decision D11: Legal Answer or Abstain Gate definition."""

from packages.decisions.ports import Question

GATE_LEGAL_OPTIONS = ["answer", "abstain", "clarify", "other"]


def build_gate_legal_question(
    query: str,
    top_score: float,
    top_citation: str,
) -> Question:
    """Construct Question for determining whether statutory grounding warrants answering or abstaining.

    Args:
        query: The founder's legal question.
        top_score: Relevance confidence score of the closest statutory match.
        top_citation: Citation reference of the candidate statute.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Legal query: '{query}'. Top retrieved statute: '{top_citation}' with confidence {top_score:.2f}. "
        "To prevent legal hallucinations, should the engine provide an answer, strictly abstain, "
        "or request clarification? Options: answer, abstain, clarify, or other."
    )
    return Question(
        id="gate_legal_answer",
        prompt=prompt,
        options=GATE_LEGAL_OPTIONS,
    )


def fail_closed_gate_legal_answer() -> str:
    """Return fail-closed decision when legal retrieval confidence is uncertain.

    Returns:
        str: Default to 'abstain' to prevent unauthorized or hallucinated legal advice.
    """
    return "abstain"
