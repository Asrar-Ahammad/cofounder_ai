# Webhook Receiver Application (`apps/webhooks`)

**Purpose:** Isolated, minimal deployable for accepting external webhook deliveries (Meta, Stripe) with signature verification and zero-latency enqueueing to Redis Streams.

## Files
- `__init__.py` — Package entrypoint.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `main.py` (6 public symbols)
  - `verify_meta_signature`: Validate Meta X-Hub-Signature-256 header in constant time.
  - `verify_stripe_signature`: Validate Stripe-Signature header timestamp and HMAC-SHA256 signature.
  - `health_check`: Liveness health check endpoint.
  - `verify_meta_webhook`: Handle Meta WhatsApp webhook subscription verification challenge.
  - `receive_meta_webhook`: Ingest WhatsApp and Meta webhooks with HMAC-SHA256 verification.
  - `receive_stripe_webhook`: Ingest Stripe subscription and billing webhooks with signature verification.

<!-- END GENERATED -->

## Running Locally
```bash
uv run uvicorn apps.webhooks.main:app --port 8001
```
