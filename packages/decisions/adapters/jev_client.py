"""TypeSafe Jev adapter for System One probabilistic decisions."""

from typing import Any

import httpx

from packages.core.errors import ExternalServiceError
from packages.decisions.ports import Decision, DecisionModel, Question


class JevClient(DecisionModel):
    """Adapter communicating with TypeSafe Jev hosted API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.typesafe.ai/v1",
        model_version: str = "jev-1.0-pinned",
    ) -> None:
        """Initialize JevClient with credentials and pinned model version.

        Args:
            api_key: Secret API key for TypeSafe Jev.
            base_url: Base endpoint URL.
            model_version: Pinned version string.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.model_version = model_version

    async def decide(
        self,
        *,
        state: dict[str, Any],
        questions: list[Question],
        timeout_ms: int = 1000,
    ) -> list[Decision]:
        """Send questions and state context to TypeSafe Jev API.

        Args:
            state: Serialized dictionary of decision context.
            questions: List of Question models.
            timeout_ms: Request timeout in milliseconds.

        Returns:
            list[Decision]: List of evaluated decisions.

        Raises:
            ExternalServiceError: If API call fails or times out.
        """
        if not self.api_key or self.api_key.startswith("jev-placeholder"):
            # Mock / fallback when running in local dev without live Jev credentials
            return [
                Decision(
                    question_id=q.id,
                    choice=q.options[0],
                    probabilities={opt: 1.0 if opt == q.options[0] else 0.0 for opt in q.options},
                    model_provider="jev-mock",
                    model_version=self.model_version,
                )
                for q in questions
            ]

        payload = {
            "model": self.model_version,
            "state": state,
            "questions": [q.model_dump() for q in questions],
        }

        try:
            async with httpx.AsyncClient(timeout=timeout_ms / 1000.0) as client:
                response = await client.post(
                    f"{self.base_url}/decide",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                response.raise_for_status()
                data = response.json()

                return [
                    Decision(
                        question_id=item["question_id"],
                        choice=item["choice"],
                        probabilities=item["probabilities"],
                        model_provider="jev",
                        model_version=self.model_version,
                    )
                    for item in data.get("decisions", [])
                ]
        except Exception as e:
            raise ExternalServiceError(f"Jev decision call failed: {e}") from e
