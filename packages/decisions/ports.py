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
