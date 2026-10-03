# 0004: Code Review Resolutions for PR #1 (Phase 0 Foundations)

## Context
During code review of Pull Request #1 on `Asrar-Ahammad/cofounder_ai`, 23 comments were submitted regarding security, data integrity, error handling, and performance boundaries.

## Decisions & Changes
1. **Decision Policy Band Classification (`packages/decisions/policy/apply_threshold.py`):**
   - High probability `block` and `injection` decisions now strictly return `ESCALATE`.
   - Approval risk decisions with choice != `low` return `CONFIRM` or `ESCALATE`.
2. **Postgres RLS Bind Parameter Support (`packages/core/db.py`):**
   - Replaced raw `SET LOCAL app.tenant_id = :tenant_id` with `SELECT set_config('app.tenant_id', :tenant_id, true)`.
3. **Egress IPv4-Mapped IPv6 Normalization (`packages/security/egress.py`):**
   - Normalized `ip_obj.ipv4_mapped` before evaluating against blocked private IPv4 networks.
4. **Decision Probability Validation (`packages/decisions/ports.py`):**
   - Added validator enforcing `0.0 <= prob <= 1.0` and `0.95 <= sum <= 1.05`.
5. **Multi-Tenant Composite Integrity & Foreign Keys (`packages/core/models/`):**
   - Added `UniqueConstraint("tenant_id", "id")` to `Venture`.
   - Added `ForeignKeyConstraint(["tenant_id", "venture_id"], ["ventures.tenant_id", "ventures.id"])` to `StoredApproval` and `StoredEvent` to prevent cross-tenant record association.
6. **Duplicate Tool Registration Protection (`packages/tools/registry.py`):**
   - `ToolRegistry.register` raises `ValueError` if a tool name is already registered.
7. **Defensive Decision History Copying (`packages/brain/service.py`):**
   - `InMemorySharedBrain.record_decision` defensively copies `evidence_refs`.
8. **Localhost Binding for Development Infrastructure (`docker-compose.yml`):**
   - Bound PostgreSQL, Redis, and Mailpit ports strictly to `127.0.0.1`.
9. **Single Source of Truth for Non-Auto Actions (`packages/approvals/service.py`):**
   - Replaced hardcoded action checks with `is_never_auto()`.
10. **Granular Approval Grants & Rejection Revocation (`packages/approvals/service.py`):**
    - Grants are keyed by tenant, venture, action, and payload hash. Rejections revoke the grant key.
11. **Frontend Approvals Inbox Real Data & Callbacks (`apps/web/components/approvals-inbox.tsx`):**
    - Removed hardcoded dummy fallback data; added async `onResolve` callback prop.
12. **Event Lineage and Timestamp Preservation (`packages/core/event_bus.py`):**
    - Preserved `occurred_at`, `causation_id`, and `correlation_id` in `consume()`.
13. **Fail-Closed on Unconfigured Decision Models (`packages/decisions/adapters/jev_client.py`):**
    - Raised `ExternalServiceError` when API key is missing, triggering fail-closed fallback.
14. **Bounded Idempotency Cache (`packages/tools/gateway.py`):**
    - Bound in-memory cache to 1000 items with LRU eviction using `OrderedDict`.

## Status
Accepted

## Consequences
All review issues are fully resolved and tested, ensuring fail-closed safety, strict multi-tenant schema isolation, and stable runtime behavior without memory leaks or credential bypasses.
