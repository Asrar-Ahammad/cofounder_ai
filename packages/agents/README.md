# Agents Package (`packages/agents`)

**Purpose:** Houses all specialist agent LangGraph subgraphs and the central Orchestrator graph. Agents are subgraphs with typed input, typed output, declared tools, and declared domain events.

## Files
- `base.py` — Base agent protocol (`Agent`), `AgentInput`, and `AgentOutput`.

## Public Functions & Classes
- `Agent`: Protocol defining name, allowed tools, consumed events, and emitted events.
- `AgentInput`: Input schema for agent execution.
- `AgentOutput`: Output schema with artifacts, events, and human intervention flags.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `base.py` (3 public symbols)
  - `AgentInput`: Input payload passed to an agent subgraph execution.
  - `AgentOutput`: Standardized output produced by an agent subgraph execution.
  - `Agent`: Protocol defining the standard interface for all specialist agents.
- `financial/__init__.py`
- `legal/__init__.py`
- `market_intel/__init__.py`
- `marketing/__init__.py`
- `operations/__init__.py`
- `orchestrator/__init__.py`
- `sales/__init__.py`
- `support/__init__.py`
- `validation/__init__.py`
- `web/__init__.py`

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/agents
```
