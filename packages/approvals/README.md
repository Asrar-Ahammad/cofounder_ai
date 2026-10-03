# Approvals Package (`packages/approvals`)

**Purpose:** Coordinates human-in-the-loop approvals, LangGraph `interrupt()` pausing, and per-tenant auto-approval policies.

## Files
- `service.py` — `ApprovalService` protocol for evaluating approval status.

## Public Functions & Classes
- `ApprovalService`: Protocol defining approval status queries for gated tools.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `service.py` (3 public symbols)
  - `ApprovalRequest`: Model representing an approval record.
  - `ApprovalService`: Protocol for managing and evaluating human approval states.
  - `InMemoryApprovalService`: In-memory approval service managing pending approvals and policies.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/approvals
```
