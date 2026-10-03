"""Unit tests for Tavily search and Firecrawl scraper adapters."""

import pytest

from packages.core.errors import PolicyViolation
from packages.integrations.adapters.firecrawl_scraper import FirecrawlScraperAdapter
from packages.integrations.adapters.tavily_search import TavilySearchAdapter


@pytest.mark.asyncio
async def test_tavily_search_adapter_mock_fallback() -> None:
    """Verify Tavily search returns structured mock results when api_key is placeholder."""
    adapter = TavilySearchAdapter(api_key="tavily-placeholder-key")
    results = await adapter.search(query="B2B AI agents", max_results=3)
    assert len(results) >= 1
    assert "title" in results[0]
    assert "url" in results[0]
    assert "snippet" in results[0]


@pytest.mark.asyncio
async def test_firecrawl_scraper_rejects_placeholder_key() -> None:
    """Verify Firecrawl scraper raises ExternalServiceError when api_key is placeholder."""
    from packages.core.errors import ExternalServiceError

    adapter = FirecrawlScraperAdapter(api_key="firecrawl-placeholder-key")
    with pytest.raises(ExternalServiceError, match="Firecrawl API key is missing"):
        await adapter.scrape(url="https://example.com/pricing")


@pytest.mark.asyncio
async def test_firecrawl_scraper_blocks_ssrf() -> None:
    """Verify Firecrawl adapter blocks SSRF to loopback and cloud metadata endpoints."""
    adapter = FirecrawlScraperAdapter(api_key="live-key")
    with pytest.raises(PolicyViolation, match="Egress blocked"):
        await adapter.scrape(url="http://169.254.169.254/latest/meta-data/")
