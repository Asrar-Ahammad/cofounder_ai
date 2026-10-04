"""Unit tests for KMS OAuth token envelope encryption and tenant isolation."""

import pytest

from packages.security.crypto import decrypt_token, encrypt_token


def test_encrypt_and_decrypt_token_success() -> None:
    """Verify sensitive token round-trip encryption and decryption."""
    raw_token = "ya29.a0AfH6SMA...google-oauth-secret-token"
    tenant_id = "tenant-prod-123"
    context = {"provider": "gmail", "user_id": "usr_456"}

    ciphertext = encrypt_token(raw_token, tenant_id=tenant_id, context=context)
    assert ciphertext != raw_token
    assert len(ciphertext) > 32

    decrypted = decrypt_token(ciphertext, tenant_id=tenant_id, context=context)
    assert decrypted == raw_token


def test_decrypt_token_fails_on_tenant_mismatch() -> None:
    """Verify tenant isolation: ciphertext cannot be decrypted under another tenant."""
    raw_token = "ayrshare_secret_api_key_xyz"
    tenant_a = "tenant-alpha"
    tenant_b = "tenant-beta"

    ciphertext = encrypt_token(raw_token, tenant_id=tenant_a)

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_token(ciphertext, tenant_id=tenant_b)


def test_decrypt_token_fails_on_context_mismatch() -> None:
    """Verify encryption context binding prevents token swapping across providers."""
    raw_token = "meta_access_token_789"
    tenant_id = "tenant-gamma"

    ciphertext = encrypt_token(raw_token, tenant_id=tenant_id, context={"provider": "meta"})

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_token(ciphertext, tenant_id=tenant_id, context={"provider": "gmail"})


def test_decrypt_token_fails_on_tampered_ciphertext() -> None:
    """Verify integrity failure when ciphertext is modified."""
    raw_token = "valid_token"
    tenant_id = "tenant-delta"

    ciphertext = encrypt_token(raw_token, tenant_id=tenant_id)
    tampered = ciphertext[:-4] + "AAAA"

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_token(tampered, tenant_id=tenant_id)
