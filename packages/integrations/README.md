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
- `ports.py` (5 public symbols)
  - `SocialPublisher`: Port for publishing social media content across platforms.
  - `EmailSender`: Port for sending transactional and outreach emails.
  - `WebSearcher`: Port for executing web searches and trend queries.
  - `WebScraper`: Port for extracting cleaned content from web pages.
  - `PaymentGateway`: Port for billing and subscription management.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/integrations
```
