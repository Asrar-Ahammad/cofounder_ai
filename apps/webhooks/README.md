# Webhook Receiver Application (`apps/webhooks`)

**Purpose:** Isolated, minimal deployable for accepting external webhook deliveries (Meta, Stripe) with signature verification and zero-latency enqueueing to Redis Streams.

## Files
- `__init__.py` — Package entrypoint.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`

<!-- END GENERATED -->

## Running Locally
```bash
uv run uvicorn apps.webhooks.main:app --port 8001
```
