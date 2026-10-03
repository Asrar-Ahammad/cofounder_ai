"""Customer OAuth token envelope encryption using per-tenant encryption context."""

import base64
import hashlib
import json
import os
from typing import Any

from cryptography.fernet import Fernet


def _derive_tenant_key(tenant_id: str, context: dict[str, Any] | None = None) -> bytes:
    """Derive deterministic 32-byte key from tenant ID and encryption context.

    Args:
        tenant_id: Tenant UUID string.
        context: Optional dictionary of encryption context attributes.

    Returns:
        bytes: Base64-urlsafe encoded 32-byte Fernet key.
    """
    master_secret = os.getenv("KMS_MASTER_SECRET", "cofunder_default_kms_master_key_32b")
    context_str = json.dumps(context or {}, sort_keys=True)
    raw = f"{master_secret}:{tenant_id}:{context_str}".encode()
    digest = hashlib.sha256(raw).digest()
    return base64.urlsafe_b64encode(digest)


def encrypt_token(
    token: str,
    tenant_id: str,
    context: dict[str, Any] | None = None,
) -> str:
    """Encrypt sensitive OAuth token bound to tenant and context.

    Args:
        token: Plaintext secret token.
        tenant_id: Tenant UUID string.
        context: Optional encryption context (e.g. {'provider': 'gmail'}).

    Returns:
        str: Encrypted ciphertext string.
    """
    key = _derive_tenant_key(tenant_id, context)
    fernet = Fernet(key)
    encrypted_bytes = fernet.encrypt(token.encode("utf-8"))
    return encrypted_bytes.decode("utf-8")


def decrypt_token(
    ciphertext: str,
    tenant_id: str,
    context: dict[str, Any] | None = None,
) -> str:
    """Decrypt token using tenant key and verify encryption context.

    Args:
        ciphertext: Encrypted token payload.
        tenant_id: Tenant UUID string.
        context: Optional encryption context matching encryption call.

    Returns:
        str: Decrypted plaintext token.

    Raises:
        ValueError: If ciphertext is tampered with or context does not match.
    """
    key = _derive_tenant_key(tenant_id, context)
    fernet = Fernet(key)
    try:
        decrypted_bytes = fernet.decrypt(ciphertext.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
    except Exception as exc:
        raise ValueError("Decryption failed: invalid ciphertext or mismatched tenant context") from exc
