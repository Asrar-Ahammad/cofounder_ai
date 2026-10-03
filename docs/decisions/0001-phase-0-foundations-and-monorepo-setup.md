# 0001 — Phase 0 Foundations, Monorepo Architecture & Tooling

- **Status:** Accepted
- **Date:** 2026-10-03
- **Author:** Antigravity AI
- **Related:** AGENTS.md, docs/architecture.md, docs/implementation_plan.md

## Context
Cofunder requires a robust, modular architecture supporting multi-agent collaboration with LangGraph, asynchronous workers, strict multi-tenant isolation via Postgres RLS, and a System One decision layer. The codebase must prevent architectural erosion (circular dependencies, cross-agent leaks, monolithic helper dump files).

## Decision
We choose:
1. **Monorepo structure** separating `apps/` (API, worker, webhooks, web) and `packages/` (`core`, `brain`, `agents`, `tools`, `integrations`, `rag`, `approvals`, `security`, `decisions`, `observability`).
2. **Layer rules enforcement** via `import-linter` in CI:
   - `core` <- `brain`, `rag`, `security` <- `integrations`, `tools`, `approvals`, `decisions` <- `agents` <- `apps`.
   - No agent may import another agent. Agents communicate solely via domain events and the Shared Brain.
3. **Packaging & Tooling**: Python 3.12 managed via `uv`, linting/formatting via `ruff`, strict type-checking via `mypy --strict`.
4. **Code granularity**: One function/class per file (`verb_noun.py`), functions < 40 lines, files < 250 lines, no `utils.py`/`helpers.py`.
5. **Living documentation**: Every package must maintain a `README.md` verified via `scripts/gen_module_index.py`.

## Alternatives considered
- **Polyrepo (separate repositories per agent/service)**: Rejected due to overhead in cross-package type synchronization, deployment coordination, and developer ergonomics in early stages.
- **Poetry / Pipenv**: Rejected in favor of `uv` for speed and deterministic lockfile generation.
- **Unrestricted package imports**: Rejected because unstructured agent code bases rapidly degrade into spaghetti dependencies.

## Why this choice
This modular monolith provides the development velocity of a single repository while strictly enforcing the isolation and dependency boundaries of microservices.

## Consequences
- Every new module must declare its exports cleanly in `__init__.py`.
- Developers must respect the layer hierarchy; violations fail CI.
- Modules remain easily testable in isolation.

## Files changed
- `pyproject.toml` — Workspace dependencies, ruff, mypy, and import-linter configurations
- `.gitignore` — Standard gitignore for Python, Node, environment variables
- `scripts/gen_module_index.py` — Living documentation sync and CI verification script
- Initial directory structure for `packages/` and `apps/`
