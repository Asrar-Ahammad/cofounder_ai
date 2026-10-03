# 0002 — Postgres RLS Multi-Tenancy & Redis Streams Event Bus

- **Status:** Accepted
- **Date:** 2026-10-03
- **Author:** Antigravity AI
- **Related:** packages/core/models, packages/core/event_bus.py, tests/security/test_tenant_isolation.py

## Context
Cofunder requires strict data isolation between startup founders across all storage layers (relational data, vector embeddings, and LangGraph checkpointer state). Cross-tenant data leakage is a critical vulnerability. Additionally, agents coordinate through asynchronous domain events (`idea_validated`, `pricing_changed`, etc.), which must be durable, order-preserved, replayable, and isolated per tenant.

## Decision
1. **PostgreSQL Row-Level Security (RLS)**:
   - Every tenant-scoped table (`ventures`, `events`, `model_decisions`, `approvals`, `artifacts`, `audit_log`) has a `tenant_id` column.
   - RLS is enabled with policies enforcing `tenant_id = current_setting('app.tenant_id')::uuid`.
   - The database session sets `SET LOCAL app.tenant_id = :tenant_id` on checkout.
2. **Redis Streams for Event Streaming**:
   - Implemented in `packages/core/event_bus.py` with consumer groups, ACK semantics, and dead-letter queue (DLQ) streams for poisonous events.
   - Consumers deduplicate based on `event.id`.

## Alternatives considered
- **Schema-per-tenant (PostgreSQL schemas)**: Rejected due to migration overhead when scaling to thousands of founders.
- **Application-only WHERE clauses**: Rejected because developer errors or SQL injection could bypass application filtering; RLS provides defense-in-depth at the database kernel level.
- **RabbitMQ / Kafka**: Redis Streams is already present in the architecture for caching/rate-limiting and handles domain event volumes cleanly with zero additional infrastructure overhead.

## Why this choice
RLS guarantees that even if application logic forgets to include `tenant_id`, Postgres will never return another tenant's records. Redis Streams provides lightweight, durable, replayable messaging.

## Consequences
- Every test and query operating on tenant data must set `app.tenant_id`.
- Automated cross-tenant tests must run in CI.

## Files changed
- `packages/core/models/` — Declarative SQLAlchemy models
- `packages/core/event_bus.py` — Redis Streams publisher & subscriber
- `tests/security/test_tenant_isolation.py` — Automated cross-tenant isolation test suite
