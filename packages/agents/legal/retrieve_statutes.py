"""Statutory retrieval node querying the canonical regulatory RAG store."""

from packages.agents.legal.state import LegalState
from packages.rag.default_corpus import load_default_legal_index

_CORPUS_STORE = load_default_legal_index()


def retrieve_relevant_statutes(state: LegalState) -> LegalState:
    """Retrieve authoritative statutory sections matching the legal query and jurisdiction.

    Args:
        state: Active Legal agent state.

    Returns:
        LegalState: State updated with retrieved chunks and citation references.
    """
    matches = _CORPUS_STORE.search(
        query=state.query,
        jurisdiction=state.jurisdiction,
        top_k=3,
        min_threshold=0.15,
    )

    chunks_data = []
    citations = []
    for match in matches:
        chunk = match.chunk
        citation = f"{chunk.act_name} Section {chunk.section_number} ({chunk.source_url})"
        chunks_data.append(
            {
                "id": chunk.id,
                "act_name": chunk.act_name,
                "section_number": chunk.section_number,
                "section_title": chunk.section_title,
                "text": chunk.text,
                "source_url": chunk.source_url,
                "score": match.score,
            }
        )
        citations.append(citation)

    state.retrieved_chunks = chunks_data
    state.citation_refs = citations
    return state
