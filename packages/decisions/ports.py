"""Ports and data models for the System One decision layer."""

from typing import Any, Protocol

from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    """A typed question presented to a System One decision model."""

    id: str = Field(..., description="Unique question identifier within this decision call")
    prompt: str = Field(..., description="Question prompt grounded in the state")
    options: list[str] = Field(..., description="Allowed choices, must include 'other'")

    @field_validator("options")
    @classmethod
    def validate_options(cls, options: list[str]) -> list[str]:
        """Verify options are non-empty and include 'other'."""
        if not options:
            raise ValueError("Options list cannot be empty")
        if "other" not in options:
            raise ValueError("Options list must include an 'other' option")
        return options


class Decision(BaseModel):
    """The outcome of a single question evaluated by the System One model."""

    question_id: str = Field(..., description="Target question ID")
    choice: str = Field(..., description="The selected option")
    probabilities: dict[str, float] = Field(
        ...,
        description="Probability distribution across all options",
    )
    model_provider: str = Field(..., description="Provider name ('jev', 'claude_haiku', etc.)")
    model_version: str = Field(..., description="Pinned model version identifier")

    @field_validator("probabilities")
    @classmethod
    def validate_probabilities(cls, probs: dict[str, float]) -> dict[str, float]:
        """Verify probabilities are between 0 and 1 and sum to ~1.0."""
        if not probs:
            raise ValueError("Probabilities dictionary cannot be empty")
        for k, v in probs.items():
            if v < 0.0 or v > 1.0:
                raise ValueError(f"Probability for '{k}' must be between 0.0 and 1.0, got {v}")
        total = sum(probs.values())
        if not (0.95 <= total <= 1.05):
            raise ValueError(f"Probabilities must sum to ~1.0, got {total}")
        return probs


class DecisionModel(Protocol):
    """Protocol for System One decision model providers."""

    async def decide(
        self,
        *,
        state: dict[str, Any],
        questions: list[Question],
        timeout_ms: int = 1000,
    ) -> list[Decision]:
        """Evaluate a batch of questions against the given state.

        Args:
            state: Dictionary containing relevant state context for the decision.
            questions: List of Question models to evaluate.
            timeout_ms: Maximum budget in milliseconds before timing out.

        Returns:
            list[Decision]: One decision per input question.
        """
        ...
