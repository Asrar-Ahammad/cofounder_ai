"""Data models for statutory documents and retrieval chunks in the RAG package."""

from pydantic import BaseModel, Field


class StatuteChunk(BaseModel):
    """Semantic statutory chunk preserving legal hierarchy and citation source."""

    model_config = {"frozen": True}

    id: str = Field(..., description="Unique chunk identifier")
    act_name: str = Field(..., description="Title of the statute or official regulation")
    jurisdiction: str = Field(..., description="Legal jurisdiction code, e.g., 'IN', 'US-DE', 'EU'")
    section_number: str = Field(..., description="Statutory section or article number")
    section_title: str = Field(..., description="Title or heading of the section")
    text: str = Field(..., description="Verbatim statutory text content")
    source_url: str = Field(..., description="Official government gazette or registry URL")
    enacted_year: int = Field(..., description="Year of enactment or notification")


class RetrievalMatch(BaseModel):
    """Ranked match result from the hybrid legal knowledge store."""

    model_config = {"frozen": True}

    chunk: StatuteChunk
    score: float = Field(..., ge=0.0, le=1.0, description="Normalized retrieval relevance score")
    match_type: str = Field(default="hybrid", description="Match type: 'vector', 'keyword', or 'hybrid'")
