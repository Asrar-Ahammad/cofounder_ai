"""LangGraph checkpointer factory for run state persistence and resumption."""

from langgraph.checkpoint.memory import MemorySaver


def get_memory_checkpointer() -> MemorySaver:
    """Initialize an in-memory checkpointer suitable for unit and integration tests.

    Returns:
        MemorySaver: Configured memory checkpointer instance.
    """
    return MemorySaver()
