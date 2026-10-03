"""Tavily search API adapter conforming to WebSearcher port."""

from typing import Any

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import WebSearcher
from packages.security.egress import validate_egress_url


class TavilySearchAdapter(WebSearcher):
    """Adapter for executing web search queries via Tavily API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.tavily.com",
    ) -> None:
        """Initialize Tavily search adapter with credentials."""
        self.api_key = api_key
        self.base_url = base_url

    async def search(
        self,
        *,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """Search the public web using Tavily Search API.

        Args:
            query: Search query text.
            max_results: Maximum count of results to return.

        Returns:
            list[dict[str, Any]]: List of results with title, url, snippet.
        """
        if not self.api_key or self.api_key.startswith("tavily-placeholder"):
            return [
                {
                    "title": f"Market search result for {query}",
                    "url": f"https://example.com/search?q={query[:20]}",
                    "snippet": f"Simulated market intelligence signal and competitor data for '{query}'.",
                }
            ]

        validate_egress_url(self.base_url)
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(f"{self.base_url}/search", json=payload)
                res.raise_for_status()
                data = res.json()
                results: list[dict[str, Any]] = []
                for item in data.get("results", []):
                    results.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "snippet": item.get("content", ""),
                        }
                    )
                return results
        except Exception as e:
            raise ExternalServiceError(f"Tavily search API error: {e}") from e
