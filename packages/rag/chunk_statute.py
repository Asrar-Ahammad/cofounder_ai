"""Statutory document parser and section hierarchy chunker."""

import re

from packages.rag.models import StatuteChunk

_SECTION_PATTERN = re.compile(
    r"(?:^|\n)(?:Section|Article)\s+([0-9A-Za-z]+)[\.\:\-\s]+([^\n]+)\n(.*?)(?=(?:\n(?:Section|Article)\s+[0-9A-Za-z]+|\Z))",
    re.DOTALL | re.IGNORECASE,
)


def chunk_statute_document(
    act_name: str,
    jurisdiction: str,
    raw_text: str,
    source_url: str,
    enacted_year: int,
) -> list[StatuteChunk]:
    """Parse raw statute text into structured chunks preserving section numbers and citations.

    Args:
        act_name: Official name of the statute.
        jurisdiction: Jurisdiction code (e.g., 'IN', 'US-DE').
        raw_text: Full verbatim text of the act or regulations.
        source_url: Authoritative gazette link.
        enacted_year: Year enacted.

    Returns:
        list[StatuteChunk]: Structured statutory chunks.
    """
    chunks: list[StatuteChunk] = []
    matches = list(_SECTION_PATTERN.finditer(raw_text))

    for match in matches:
        sec_num = match.group(1).strip()
        sec_title = match.group(2).strip()
        body = match.group(3).strip()

        chunk_id = f"{jurisdiction}_{act_name.lower().replace(' ', '_')}_s{sec_num}"
        chunks.append(
            StatuteChunk(
                id=chunk_id,
                act_name=act_name,
                jurisdiction=jurisdiction,
                section_number=sec_num,
                section_title=sec_title,
                text=body if body else sec_title,
                source_url=source_url,
                enacted_year=enacted_year,
            )
        )

    if not chunks and raw_text.strip():
        # Fallback single chunk if no section markers matched
        slug = act_name.lower().replace(" ", "_")
        chunks.append(
            StatuteChunk(
                id=f"{jurisdiction}_{slug}_main",
                act_name=act_name,
                jurisdiction=jurisdiction,
                section_number="General",
                section_title="Full Statute Overview",
                text=raw_text.strip(),
                source_url=source_url,
                enacted_year=enacted_year,
            )
        )

    return chunks
