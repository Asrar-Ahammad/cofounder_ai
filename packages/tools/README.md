# Tools Package (`packages/tools`)

**Purpose:** Defines the central Tool Gateway and Tool Registry. Every external side effect passes through the Tool Gateway for allowlist verification, argument schema validation, idempotency checks, and approval gating.

## Files
- `gateway.py` — `ToolGateway` class controlling execution and security policies.
- `registry.py` — `ToolSpec` and `ToolRegistry` managing registered capabilities.

## Public Functions & Classes
- `ToolGateway`: Choke-point enforcing allowlists, argument validation, approvals, and idempotency.
- `ToolRegistry`: In-memory registry storing tool definitions.
- `ToolSpec`: Specification of a callable tool, its Pydantic args model, and its policies.
- `tool_registry`: Default singleton instance of `ToolRegistry`.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `gateway.py` (1 public symbols)
  - `ToolGateway`: Central gateway enforcing security, schemas, approvals, and idempotency.
- `registry.py` (2 public symbols)
  - `ToolSpec`: Specification describing a callable tool, its schema, and its requirements.
  - `ToolRegistry`: In-memory registry of all available tools across Cofunder.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/tools
```
