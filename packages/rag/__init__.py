"""Legal and regulatory RAG package for statutory indexing and citation retrieval."""

from packages.rag.chunk_statute import chunk_statute_document
from packages.rag.default_corpus import load_default_legal_index
from packages.rag.index_store import StatuteIndexStore
from packages.rag.models import RetrievalMatch, StatuteChunk

__all__ = [
    "RetrievalMatch",
    "StatuteChunk",
    "StatuteIndexStore",
    "chunk_statute_document",
    "load_default_legal_index",
]
