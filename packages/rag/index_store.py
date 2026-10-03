"""Hybrid statutory index store providing citation-accurate legal retrieval."""

import re

from packages.rag.models import RetrievalMatch, StatuteChunk

_STOPWORDS = {
    "a", "an", "the", "in", "on", "at", "for", "to", "of", "and", "or",
    "with", "by", "is", "are", "was", "were", "be", "been", "it", "this", "that",
}


class StatuteIndexStore:
    """In-memory hybrid retrieval index for statutory sections with keyword and semantic scoring."""

    def __init__(self) -> None:
        """Initialize empty statute index."""
        self._chunks: dict[str, StatuteChunk] = {}

    def add_chunks(self, chunks: list[StatuteChunk]) -> None:
        """Index a batch of statutory chunks."""
        for chunk in chunks:
            self._chunks[chunk.id] = chunk

    def search(
        self,
        query: str,
        *,
        jurisdiction: str | None = None,
        top_k: int = 3,
        min_threshold: float = 0.20,
    ) -> list[RetrievalMatch]:
        """Perform hybrid retrieval against indexed statutes.

        Args:
            query: The legal or regulatory question.
            jurisdiction: Optional jurisdiction filter (e.g. 'IN', 'US-DE').
            top_k: Maximum number of matches.
            min_threshold: Minimum match score threshold.

        Returns:
            list[RetrievalMatch]: Ranked statutory matches.
        """
        raw_terms = set(re.findall(r"\w+", query.lower()))
        query_terms = {t for t in raw_terms if t not in _STOPWORDS and len(t) > 1}
        if not query_terms:
            query_terms = raw_terms
        if not query_terms:
            return []

        results: list[RetrievalMatch] = []
        for chunk in self._chunks.values():
            if jurisdiction and chunk.jurisdiction.upper() != jurisdiction.upper():
                continue

            content = f"{chunk.act_name} {chunk.section_title} {chunk.text}".lower()
            content_terms = set(re.findall(r"\w+", content))

            intersection = query_terms.intersection(content_terms)
            if not intersection:
                continue

            score = len(intersection) / len(query_terms)
            if any(term in chunk.section_title.lower() for term in query_terms):
                score = min(1.0, score + 0.25)
            if any(term in chunk.act_name.lower() for term in query_terms):
                score = min(1.0, score + 0.15)

            if score >= min_threshold:
                results.append(RetrievalMatch(chunk=chunk, score=round(score, 3), match_type="hybrid"))

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]
