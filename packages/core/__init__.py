"""Core module for Cofunder containing domain models, errors, and database engine."""

from packages.core.config import Settings, get_settings
from packages.core.context import AgentContext, AgentInfo
from packages.core.db import get_db_engine, get_db_session, get_session_factory
from packages.core.errors import (
    ApprovalRequired,
    CofunderError,
    ExternalServiceError,
    PolicyViolation,
    TenantIsolationError,
    ValidationError,
)
from packages.core.event_bus import EventBus
from packages.core.events import DomainEvent

__all__ = [
    "AgentContext",
    "AgentInfo",
    "ApprovalRequired",
    "CofunderError",
    "DomainEvent",
    "EventBus",
    "ExternalServiceError",
    "PolicyViolation",
    "Settings",
    "TenantIsolationError",
    "ValidationError",
    "get_db_engine",
    "get_db_session",
    "get_session_factory",
    "get_settings",
]
