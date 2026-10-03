# Brain Package (`packages/brain`)

**Purpose:** Implements the Shared Brain service, managing venture profiles, versioned business constraints, the immutable decision log, and LangGraph Postgres checkpointer state.

## Files
- `service.py` — Protocols and models: `VentureProfile`, `VentureConstraints`, and `SharedBrain`.

## Public Functions & Classes
- `SharedBrain`: Central protocol for accessing venture knowledge and recording decisions.
- `VentureProfile`: Aggregate venture data model.
- `VentureConstraints`: Financial and volume caps enforced on agent operations.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `checkpointer.py` (1 public symbols)
  - `get_memory_checkpointer`: Initialize an in-memory checkpointer suitable for unit and integration tests.
- `repository.py` (1 public symbols)
  - `BrainRepository`: Async database repository for Shared Brain state aggregates.
- `service.py` (4 public symbols)
  - `VentureProfile`: Venture profile aggregate managed by the Shared Brain.
  - `VentureConstraints`: Structured constraints governing agent budgets and outreach caps.
  - `SharedBrain`: Protocol for Shared Brain read and write operations.
  - `InMemorySharedBrain`: In-memory implementation of the Shared Brain for tests and local execution.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/brain
```
