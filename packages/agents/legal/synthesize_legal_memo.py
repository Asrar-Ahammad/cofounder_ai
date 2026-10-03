"""Legal memorandum synthesis node generating grounded analysis, clarification, or formal abstention."""

from packages.agents.legal.state import LegalState


def synthesize_legal_memorandum(state: LegalState) -> LegalState:
    """Generate structured statutory memorandum with explicit section/article citations.

    Args:
        state: Active Legal agent state.

    Returns:
        LegalState: State updated with legal memorandum analysis and summary.
    """
    if state.decision == "abstain":
        state.analysis = (
            f"ABSTENTION: No authoritative statutory provisions in the verified corpus for "
            f"jurisdiction '{state.jurisdiction}' meet the mandatory confidence threshold to answer: "
            f"'{state.query}'. To avoid hallucinating regulatory requirements, Cofunder AI strictly "
            f"abstains from advising on this question. Please consult a licensed attorney in {state.jurisdiction}."
        )
        state.summary = f"Legal agent strictly abstained on out-of-corpus query: '{state.query}'."
        return state

    if state.decision == "clarify":
        state.analysis = (
            f"CLARIFICATION REQUIRED: The query '{state.query}' has ambiguous statutory overlap "
            f"in jurisdiction '{state.jurisdiction}'. Please clarify the specific regulatory scope "
            "(e.g., data privacy consent, corporate formation, or registered office filings)."
        )
        state.summary = f"Legal agent requested statutory scope clarification for query: '{state.query}'."
        return state

    # Synthesize grounded answer
    lines = [f"# Statutory Compliance Synthesis: {state.query}", ""]
    for chunk in state.retrieved_chunks:
        act = chunk["act_name"]
        sec = chunk["section_number"]
        sec_type = chunk.get("section_type", "Section")
        title = chunk["section_title"]
        text = chunk["text"]
        url = chunk["source_url"]
        lines.append(f"### {act} — {sec_type} {sec}: {title}")
        lines.append(f"> \"{text}\"")
        lines.append(f"*Source: [{url}]({url})*\n")

    lines.append(f"\n---\n**Notice:** {state.disclaimer}")
    state.analysis = "\n".join(lines)
    state.summary = f"Synthesized grounded statutory memorandum citing {len(state.citation_refs)} sections."
    return state
