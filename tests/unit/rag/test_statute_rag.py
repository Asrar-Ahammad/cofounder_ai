"""Unit tests for statutory RAG chunking and hybrid retrieval."""

from packages.rag.chunk_statute import chunk_statute_document
from packages.rag.default_corpus import load_default_legal_index


def test_chunk_statute_document_extracts_sections() -> None:
    """Verify regex chunker accurately extracts statutory section numbers and citations."""
    sample_statute = """
Section 1 Short title and commencement
This Act may be called the Digital Personal Data Protection Act, 2023.

Section 2 Definitions
In this Act, unless the context otherwise requires, Data Principal means the individual.
"""
    chunks = chunk_statute_document(
        act_name="DPDP Act",
        jurisdiction="IN",
        raw_text=sample_statute,
        source_url="https://example.gov.in/act",
        enacted_year=2023,
    )
    assert len(chunks) == 2
    assert chunks[0].section_number == "1"
    assert chunks[0].section_title == "Short title and commencement"
    assert "Digital Personal Data Protection Act" in chunks[0].text
    assert chunks[0].source_url == "https://example.gov.in/act"

    assert chunks[1].section_number == "2"
    assert chunks[1].section_title == "Definitions"


def test_statute_index_store_search_and_jurisdiction_filter() -> None:
    """Verify hybrid search returns relevant matches and filters by jurisdiction."""
    store = load_default_legal_index()

    # Query for DPDP in India
    in_matches = store.search("grounds for processing personal data consent", jurisdiction="IN")
    assert len(in_matches) > 0
    top_chunk = in_matches[0].chunk
    assert top_chunk.jurisdiction == "IN"
    assert top_chunk.section_number in ("4", "6")
    assert top_chunk.source_url.startswith("https://")

    # Query for Delaware incorporation
    de_matches = store.search("certificate of incorporation registered office", jurisdiction="US-DE")
    assert len(de_matches) > 0
    assert de_matches[0].chunk.jurisdiction == "US-DE"
    assert "Delaware" in de_matches[0].chunk.act_name

    # Empty match for non-existent topic
    empty_matches = store.search("astronomy telescope orbital decay", jurisdiction="IN")
    assert len(empty_matches) == 0

    # Query for Companies Act 2013
    ca_matches = store.search("incorporation of company memorandum articles", jurisdiction="IN")
    assert len(ca_matches) > 0
    assert any("Companies Act" in m.chunk.act_name for m in ca_matches)


def test_chunk_statute_document_extracts_articles() -> None:
    """Verify regex chunker accurately identifies Article vs Section."""
    gdpr_sample = """
Article 5 Principles relating to processing of personal data
Personal data shall be processed lawfully, fairly and in a transparent manner.

Article 6 Lawfulness of processing
Processing shall be lawful only if and to the extent that at least one condition applies.
"""
    chunks = chunk_statute_document(
        act_name="GDPR",
        jurisdiction="EU",
        raw_text=gdpr_sample,
        source_url="https://gdpr-info.eu/art-5-gdpr/",
        enacted_year=2016,
    )
    assert len(chunks) == 2
    assert chunks[0].section_type == "Article"
    assert chunks[0].section_number == "5"
    assert chunks[0].citation == "GDPR, Article 5 (2016)"
    assert chunks[1].section_type == "Article"
    assert chunks[1].section_number == "6"
