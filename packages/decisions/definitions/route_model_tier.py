"""Decision D4: LLM Model Tier Routing definition."""

from packages.decisions.ports import Question

MODEL_TIER_OPTIONS = ["haiku", "sonnet", "opus", "no_llm_needed", "other"]


def build_model_tier_question(task_complexity: str, context_length: int) -> Question:
    """Construct Question for choosing LLM tier based on task complexity and budget.

    Args:
        task_complexity: Description of reasoning depth needed.
        context_length: Approximate token count of context.

    Returns:
        Question: Validated Question model.
    """
    prompt = (
        f"Select LLM tier for task. Complexity: {task_complexity[:300]}. "
        f"Context size: {context_length} tokens. "
        "Choose optimal tier: haiku (fast/cheap), sonnet (reasoning), opus (deep research), or no_llm_needed."
    )
    return Question(
        id="route_model_tier",
        prompt=prompt,
        options=MODEL_TIER_OPTIONS,
    )


def fail_closed_model_tier() -> str:
    """Return fail-safe tier when decision model is unavailable.

    Returns:
        str: Default to balanced 'sonnet' tier.
    """
    return "sonnet"
