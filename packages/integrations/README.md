# Integrations Package (`packages/integrations`)

**Purpose:** Defines abstract port interfaces and concrete third-party adapters (Ayrshare, Meta, Gmail, Stripe, Tavily, Firecrawl).

## Files
- `ports.py` — Protocols and abstract interfaces for external side-effect services.

## Public Functions & Classes
- `SocialPublisher`: Protocol for multi-platform social media publishing.
- `EmailSender`: Protocol for transactional and outreach email delivery.
- `WebSearcher`: Protocol for web search queries.
- `WebScraper`: Protocol for URL content extraction.
- `PaymentGateway`: Protocol for Stripe checkout and billing operations.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `adapters/__init__.py`
- `adapters/ayrshare.py` (1 public symbols)
  - `AyrshareSocialAdapter`: Adapter publishing posts across social networks via Ayrshare API.
- `adapters/calcom.py` (1 public symbols)
  - `CalComCalendarAdapter`: Adapter interacting with Cal.com API for appointment booking.
- `adapters/firecrawl_scraper.py` (1 public symbols)
  - `FirecrawlScraperAdapter`: Adapter for scraping and markdown conversion via Firecrawl API.
- `adapters/gmail.py` (1 public symbols)
  - `GmailEmailAdapter`: Adapter for sending personalized outreach emails via Gmail API.
- `adapters/tavily_search.py` (1 public symbols)
  - `TavilySearchAdapter`: Adapter for executing web search queries via Tavily API.
- `ports.py` (6 public symbols)
  - `SocialPublisher`: Port for publishing social media content across platforms.
  - `EmailSender`: Port for sending transactional and outreach emails.
  - `WebSearcher`: Port for executing web searches and trend queries.
  - `WebScraper`: Port for extracting cleaned content from web pages.
  - `PaymentGateway`: Port for billing and subscription management.
  - `CalendarScheduler`: Port for calendar booking and availability synchronization.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/integrations
```
