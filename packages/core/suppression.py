"""Suppression list registry preventing unwanted outbound communications."""

import json
import os
import threading
from pathlib import Path

_lock = threading.Lock()
_SUPPRESSED_EMAILS: dict[str, set[str]] = {}
_SUPPRESSION_REASONS: dict[str, dict[str, str]] = {}
_STORE_PATH: Path | None = None
_LOADED: bool = False



def set_suppression_store_path(path: str | Path | None) -> None:
    """Set optional persistent store file path for suppression registry.

    Args:
        path: File path string or Path object, or None to disable persistence.
    """
    global _STORE_PATH, _LOADED
    with _lock:
        _STORE_PATH = Path(path) if path else None
        _LOADED = False


def _get_store_path() -> Path | None:
    """Return active storage file path from environment or configured path."""
    if _STORE_PATH is not None:
        return _STORE_PATH
    env_path = os.getenv("SUPPRESSION_STORE_PATH")
    return Path(env_path) if env_path else None


def _load_persisted() -> None:
    """Load persisted suppression registry from storage file into memory cache."""
    global _LOADED
    if _LOADED:
        return
    _LOADED = True
    path = _get_store_path()
    if not path or not path.exists():
        return
    try:
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)
        for tid, emails in data.get("emails", {}).items():
            _SUPPRESSED_EMAILS.setdefault(tid, set()).update(emails)
        for tid, reasons in data.get("reasons", {}).items():
            _SUPPRESSION_REASONS.setdefault(tid, {}).update(reasons)
    except Exception:
        pass


def _save_persisted() -> None:
    """Persist in-memory suppression registry to storage file atomically."""
    path = _get_store_path()
    if not path:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "emails": {tid: sorted(emails) for tid, emails in _SUPPRESSED_EMAILS.items()},
            "reasons": _SUPPRESSION_REASONS,
        }
        tmp_path = path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp_path.replace(path)
    except Exception:
        pass


def add_to_suppression_list(tenant_id: str, email: str, reason: str = "unsubscribe") -> None:
    """Add an email address to the tenant's suppression list.

    Args:
        tenant_id: Tenant UUID string.
        email: Email address to suppress.
        reason: Reason for suppression (e.g. 'unsubscribe', 'complaint', 'manual').
    """
    with _lock:
        _load_persisted()
        normalized = email.strip().lower()
        if tenant_id not in _SUPPRESSED_EMAILS:
            _SUPPRESSED_EMAILS[tenant_id] = set()
            _SUPPRESSION_REASONS[tenant_id] = {}
        _SUPPRESSED_EMAILS[tenant_id].add(normalized)
        _SUPPRESSION_REASONS[tenant_id][normalized] = reason
        _save_persisted()


def is_email_suppressed(tenant_id: str, email: str) -> bool:
    """Check if an email address is suppressed from outbound communications.

    Args:
        tenant_id: Tenant UUID string.
        email: Target email address.

    Returns:
        bool: True if email is suppressed, False otherwise.
    """
    with _lock:
        _load_persisted()
        normalized = email.strip().lower()
        return normalized in _SUPPRESSED_EMAILS.get(tenant_id, set())


def clear_suppression_list(tenant_id: str | None = None) -> None:
    """Clear suppression registry (primarily for unit test isolation).

    Args:
        tenant_id: Optional tenant to clear; if None, clears all tenants.
    """
    with _lock:
        _load_persisted()
        if tenant_id:
            _SUPPRESSED_EMAILS.pop(tenant_id, None)
            _SUPPRESSION_REASONS.pop(tenant_id, None)
        else:
            _SUPPRESSED_EMAILS.clear()
            _SUPPRESSION_REASONS.clear()
        _save_persisted()

