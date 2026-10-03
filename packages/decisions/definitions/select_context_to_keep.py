"""Decision D10: Context Compaction selection definition."""

from packages.decisions.ports import Question

CONTEXT_COMPACTION_OPTIONS = [
    "keep_all",
    "summarize_older",
    "drop_tool_details",
    "other",
]


def build_context_compaction_question(current_token_count: int, threshold_tokens: int) -> Question:
    """Construct Question to decide context management strategy when approaching limit.

    Args:
        current_token_count: Current context size in tokens.
        threshold_tokens: Maximum budget threshold.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Context usage: {current_token_count}/{threshold_tokens} tokens. "
        "Select compaction strategy: keep_all, summarize_older, drop_tool_details, or other."
    )
    return Question(
        id="select_context_to_keep",
        prompt=prompt,
        options=CONTEXT_COMPACTION_OPTIONS,
    )


def fail_closed_context_compaction() -> str:
    """Return fallback compaction strategy.

    Returns:
        str: Default to 'summarize_older' to safely conserve context window without losing memory.
    """
    return "summarize_older"
