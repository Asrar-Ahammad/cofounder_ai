"""Unit tests for isolated Webhook Receiver deployable."""

import hashlib
import hmac
import time

from fastapi.testclient import TestClient

from apps.webhooks.main import app, verify_meta_signature, verify_stripe_signature

client = TestClient(app)


def test_health_check() -> None:
    """Verify webhook receiver liveness endpoint."""
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "webhooks"}


def test_meta_webhook_challenge_success() -> None:
    """Verify Meta webhook challenge verification succeeds with valid token."""
    res = client.get(
        "/webhooks/meta",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "cofunder_meta_verify_token",
            "hub.challenge": "1158201444",
        },
    )
    assert res.status_code == 200
    assert res.text == "1158201444"


def test_meta_webhook_challenge_forbidden_on_mismatch() -> None:
    """Verify Meta webhook challenge fails with 403 on invalid token."""
    res = client.get(
        "/webhooks/meta",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong_token",
            "hub.challenge": "1158201444",
        },
    )
    assert res.status_code == 403


def test_meta_webhook_signature_verification() -> None:
    """Verify Meta HMAC-SHA256 signature validation."""
    secret = "test_meta_app_secret"
    payload = b'{"object": "whatsapp_business_account", "entry": []}'
    sig = hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()

    assert verify_meta_signature(payload, f"sha256={sig}", secret) is True
    assert verify_meta_signature(payload, "sha256=invalid_hex_signature", secret) is False
    assert verify_meta_signature(payload, None, secret) is False


def test_stripe_webhook_signature_verification() -> None:
    """Verify Stripe timestamped HMAC-SHA256 signature validation."""
    secret = "whsec_test_stripe_secret"
    payload = b'{"type": "customer.subscription.created", "id": "sub_123"}'
    now = int(time.time())
    signed_payload = f"{now}.{payload.decode('utf-8')}".encode()
    sig = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    header = f"t={now},v1={sig}"

    assert verify_stripe_signature(payload, header, secret) is True

    # Forged signature
    assert verify_stripe_signature(payload, f"t={now},v1=forged_signature", secret) is False

    # Expired timestamp (older than tolerance)
    old_time = now - 600
    old_signed = f"{old_time}.{payload.decode('utf-8')}".encode()
    old_sig = hmac.new(secret.encode("utf-8"), old_signed, hashlib.sha256).hexdigest()
    assert verify_stripe_signature(payload, f"t={old_time},v1={old_sig}", secret, tolerance=300) is False
