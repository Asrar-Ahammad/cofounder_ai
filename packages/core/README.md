# Core Package (`packages/core`)

**Purpose:** Pure domain models, application configuration, domain events, errors, and async database engine. Contains no third-party I/O or vendor adapters.

## Files
- `config.py` — Global application configuration via Pydantic Settings.
- `context.py` — Immutable agent and tool execution context models.
- `db.py` — SQLAlchemy 2.0 async engine and session factory with Postgres RLS support.
- `errors.py` — Domain error hierarchy rooted in `CofunderError`.
- `events.py` — Immutable `DomainEvent` Pydantic model for event streams.

## Public Functions & Classes
- `Settings`: Validated settings model loaded from environment.
- `get_settings() -> Settings`: Returns global configuration instance.
- `AgentContext`: Immutable execution context passed to agent nodes and tools.
- `AgentInfo`: Metadata describing an executing agent.
- `get_db_engine() -> AsyncEngine`: Singleton SQLAlchemy async engine.
- `get_db_session(tenant_id=None) -> AsyncGenerator[AsyncSession, None]`: Context manager for transactional DB sessions.
- `DomainEvent`: Frozen Pydantic model representing domain events.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `config.py` (2 public symbols)
  - `Settings`: Global configuration settings for Cofunder services.
  - `get_settings`: Retrieve validated application settings instance.
- `constraints.py` (4 public symbols)
  - `ConstraintLimits`: Immutable business boundaries configured for a venture.
  - `validate_spend_proposal`: Enforce spending does not exceed the venture's monthly budget cap.
  - `validate_cac_proposal`: Enforce estimated customer acquisition cost does not exceed CAC ceiling.
  - `validate_outreach_proposal`: Enforce outbound volume does not exceed daily messaging cap.
- `context.py` (2 public symbols)
  - `AgentInfo`: Metadata describing an executing agent.
  - `AgentContext`: Immutable context passed into agent nodes and tool invocations.
- `db.py` (3 public symbols)
  - `get_db_engine`: Retrieve or initialize the singleton SQLAlchemy async engine.
  - `get_session_factory`: Retrieve or initialize the singleton SQLAlchemy async session maker.
  - `get_db_session`: Provide a transactional async session with tenant isolation set if provided.
- `errors.py` (6 public symbols)
  - `CofunderError`: Base exception for all domain errors in Cofunder.
  - `ValidationError`: Raised when data or argument fails schema or semantic validation.
  - `PolicyViolation`: Raised when an operation violates security, tenancy, or financial constraints.
  - `ApprovalRequired`: Raised when a tool or action cannot proceed without human confirmation.
  - `ExternalServiceError`: Raised when an external third-party adapter call fails.
  - `TenantIsolationError`: Raised when an operation attempts unauthorized cross-tenant data access.
- `event_bus.py` (1 public symbols)
  - `EventBus`: Redis Streams publisher and subscriber for multi-tenant domain events.
- `events.py` (1 public symbols)
  - `DomainEvent`: Immutable domain event model published to Redis Streams.
- `models/__init__.py`
- `models/approval.py` (1 public symbols)
  - `StoredApproval`: Pending and historic approval requests.
- `models/base.py` (1 public symbols)
  - `Base`: Base class for all database models.
- `models/constraint.py` (1 public symbols)
  - `Constraint`: Versioned business and spending limits for a venture.
- `models/event.py` (1 public symbols)
  - `StoredEvent`: Append-only domain event log table with RLS.
- `models/model_decision.py` (1 public symbols)
  - `ModelDecision`: Immutable log of probabilistic decisions made by System One models.
- `models/tenant.py` (1 public symbols)
  - `Tenant`: Customer tenant aggregate root.
- `models/venture.py` (1 public symbols)
  - `Venture`: Venture aggregate root protected by Row-Level Security.
- `suppression.py` (3 public symbols)
  - `add_to_suppression_list`: Add an email address to the tenant's suppression list.
  - `is_email_suppressed`: Check if an email address is suppressed from outbound communications.
  - `clear_suppression_list`: Clear suppression registry (primarily for unit test isolation).

<!-- END GENERATED -->

## Config / Env Vars
- `DATABASE_URL`: Connection string for PostgreSQL (psycopg3 async).
- `REDIS_URL`: Redis connection URL.
- `ENVIRONMENT`: Runtime environment (`development`, `staging`, `production`).

## Testing
```bash
pytest tests/unit/core
```
