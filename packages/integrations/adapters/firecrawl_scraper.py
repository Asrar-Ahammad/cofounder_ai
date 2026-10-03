"""Firecrawl scraper adapter conforming to WebScraper port."""

from typing import Any

import httpx

from packages.core.errors import ExternalServiceError
from packages.integrations.ports import WebScraper
from packages.security.egress import validate_egress_url


class FirecrawlScraperAdapter(WebScraper):
    """Adapter for scraping and markdown conversion via Firecrawl API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.firecrawl.dev/v1",
    ) -> None:
        """Initialize Firecrawl scraper adapter with credentials."""
        self.api_key = api_key
        self.base_url = base_url

    async def scrape(
        self,
        *,
        url: str,
    ) -> dict[str, Any]:
        """Scrape webpage content and convert to structured markdown.

        Args:
            url: The HTTP(S) URL to extract content from.

        Returns:
            dict[str, Any]: Scraped content dictionary.
        """
        validate_egress_url(url)

        if not self.api_key or self.api_key.startswith("firecrawl-placeholder"):
            return {
                "url": url,
                "title": f"Scraped page for {url}",
                "markdown": f"# Page Content\nSimulated competitor and pricing data extracted from {url}.",
                "metadata": {"status": "mock"},
            }

        validate_egress_url(self.base_url)
        payload = {"url": url, "formats": ["markdown"]}
        headers = {"Authorization": f"Bearer {self.api_key}"}

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                res = await client.post(
                    f"{self.base_url}/scrape",
                    json=payload,
                    headers=headers,
                )
                res.raise_for_status()
                data = res.json()
                page_data = data.get("data", {})
                return {
                    "url": url,
                    "title": page_data.get("metadata", {}).get("title", ""),
                    "markdown": page_data.get("markdown", ""),
                    "metadata": page_data.get("metadata", {}),
                }
        except Exception as e:
            raise ExternalServiceError(f"Firecrawl scrape API error: {e}") from e
