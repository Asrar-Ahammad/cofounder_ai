"""Isolated, minimal FastAPI deployable for external webhook ingestion."""

import hashlib
import hmac
import json
import logging
import os
import time

from fastapi import FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.responses import PlainTextResponse

_logger = logging.getLogger("cofunder.webhooks")
app = FastAPI(title="Cofunder Webhook Receiver", version="1.0.0")


def verify_meta_signature(raw_body: bytes, signature_header: str | None, app_secret: str) -> bool:
    """Validate Meta X-Hub-Signature-256 header in constant time."""
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature_header)


def verify_stripe_signature(
    raw_body: bytes,
    signature_header: str | None,
    secret: str,
    tolerance: int = 300,
) -> bool:
    """Validate Stripe-Signature header timestamp and HMAC-SHA256 signature."""
    if not signature_header:
        return False
    parts = dict(item.strip().split("=", 1) for item in signature_header.split(",") if "=" in item)
    timestamp, received_sig = parts.get("t"), parts.get("v1")
    if not timestamp or not received_sig:
        return False
    try:
        t_int = int(timestamp)
        if abs(time.time() - t_int) > tolerance:
            return False
    except ValueError:
        return False
    signed_payload = f"{timestamp}.{raw_body.decode('utf-8', errors='replace')}".encode()
    computed = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed, received_sig)


@app.get("/health")
@app.get("/livez")
async def health_check() -> dict[str, str]:
    """Liveness health check endpoint."""
    return {"status": "ok", "service": "webhooks"}


@app.get("/webhooks/meta")
async def verify_meta_webhook(
    mode: str = Query(alias="hub.mode", default=""),
    token: str = Query(alias="hub.verify_token", default=""),
    challenge: str = Query(alias="hub.challenge", default=""),
) -> Response:
    """Handle Meta WhatsApp webhook subscription verification challenge."""
    verify_token = os.getenv("META_WEBHOOK_VERIFY_TOKEN", "cofunder_meta_verify_token")
    if mode == "subscribe" and hmac.compare_digest(token, verify_token):
        return PlainTextResponse(content=challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Verification token mismatch")


@app.post("/webhooks/meta")
async def receive_meta_webhook(
    request: Request,
    x_hub_signature_256: str | None = Header(default=None, alias="X-Hub-Signature-256"),
) -> dict[str, str]:
    """Ingest WhatsApp and Meta webhooks with HMAC-SHA256 verification."""
    raw_body = await request.body()
    app_secret = os.getenv("META_APP_SECRET", "meta_app_secret_placeholder")

    if not verify_meta_signature(raw_body, x_hub_signature_256, app_secret):
        raise HTTPException(status_code=401, detail="Invalid Meta signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        payload = {"raw": raw_body.decode("utf-8", errors="replace")}

    _logger.info("Enqueued Meta webhook: event=%s", payload.get("object", "unknown"))
    return {"status": "received", "channel": "meta"}


@app.post("/webhooks/stripe")
async def receive_stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="Stripe-Signature"),
) -> dict[str, str]:
    """Ingest Stripe subscription and billing webhooks with signature verification."""
    raw_body = await request.body()
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_stripe_placeholder")

    if not verify_stripe_signature(raw_body, stripe_signature, secret):
        raise HTTPException(status_code=401, detail="Invalid Stripe signature")

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        payload = {"raw": raw_body.decode("utf-8", errors="replace")}

    _logger.info("Enqueued Stripe webhook: type=%s", payload.get("type", "unknown"))
    return {"status": "received", "channel": "stripe"}
