# RAG Package (`packages/rag`)

**Purpose:** Document parsing (PyMuPDF), semantic chunking, pgvector HNSW indexing, and citation verification for the Legal & Compliance agent.

## Files
- `__init__.py` — Package entrypoint.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `chunk_statute.py` (1 public symbols)
  - `chunk_statute_document`: Parse raw statute text into structured chunks preserving section numbers and citations.
- `default_corpus.py` (1 public symbols)
  - `load_default_legal_index`: Build and populate a default StatuteIndexStore with standard venture statutes.
- `index_store.py` (1 public symbols)
  - `StatuteIndexStore`: In-memory hybrid retrieval index for statutory sections with keyword and semantic scoring.
- `models.py` (2 public symbols)
  - `StatuteChunk`: Semantic statutory chunk preserving legal hierarchy and citation source.
  - `RetrievalMatch`: Ranked match result from the hybrid legal knowledge store.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/rag
```
