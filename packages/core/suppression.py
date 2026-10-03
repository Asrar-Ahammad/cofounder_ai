"""Suppression list registry preventing unwanted outbound communications."""

import threading

_lock = threading.Lock()
_SUPPRESSED_EMAILS: dict[str, set[str]] = {}
_SUPPRESSION_REASONS: dict[str, dict[str, str]] = {}


def add_to_suppression_list(tenant_id: str, email: str, reason: str = "unsubscribe") -> None:
    """Add an email address to the tenant's suppression list.

    Args:
        tenant_id: Tenant UUID string.
        email: Email address to suppress.
        reason: Reason for suppression (e.g. 'unsubscribe', 'complaint', 'manual').
    """
    with _lock:
        normalized = email.strip().lower()
        if tenant_id not in _SUPPRESSED_EMAILS:
            _SUPPRESSED_EMAILS[tenant_id] = set()
            _SUPPRESSION_REASONS[tenant_id] = {}
        _SUPPRESSED_EMAILS[tenant_id].add(normalized)
        _SUPPRESSION_REASONS[tenant_id][normalized] = reason


def is_email_suppressed(tenant_id: str, email: str) -> bool:
    """Check if an email address is suppressed from outbound communications.

    Args:
        tenant_id: Tenant UUID string.
        email: Target email address.

    Returns:
        bool: True if email is suppressed, False otherwise.
    """
    with _lock:
        normalized = email.strip().lower()
        return normalized in _SUPPRESSED_EMAILS.get(tenant_id, set())


def clear_suppression_list(tenant_id: str | None = None) -> None:
    """Clear suppression registry (primarily for unit test isolation).

    Args:
        tenant_id: Optional tenant to clear; if None, clears all tenants.
    """
    with _lock:
        if tenant_id:
            _SUPPRESSED_EMAILS.pop(tenant_id, None)
            _SUPPRESSION_REASONS.pop(tenant_id, None)
        else:
            _SUPPRESSED_EMAILS.clear()
            _SUPPRESSION_REASONS.clear()
