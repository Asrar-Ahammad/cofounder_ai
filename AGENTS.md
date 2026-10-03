# Agent Instructions for Cofunder

## Code Structure
- One function/class/node/tool/prompt per file, named for what it does (`verb_noun.py`). No `utils.py`, `helpers.py`, or `common.py`.
- Functions < 40 lines, files < 250 lines. Pure logic separate from I/O.
- Depend on interfaces in `packages/integrations/ports.py`, never on vendor SDKs directly.
- Respect the layer rules: `core` <- `brain`, `rag`, `security` <- `integrations`, `tools`, `approvals`, `decisions` <- `agents` <- `apps`.
- Never import across agents. Agents communicate through events and the Shared Brain.

## Frontend Rules
- Next.js 15 (App Router) + React 19 + TypeScript (strict) + Tailwind CSS 4 + shadcn/ui.
- **Typography:** Always use **Inter** font via `next/font/google` (`--font-inter`) on the root layout.
- Strictly validate API boundaries using `openapi-typescript` generated types.

## Before You Write Code
1. Read the module's `README.md` and relevant files in `docs/decisions/`.
2. For any non-trivial change, create `docs/decisions/NNNN-title.md` (use the ADR template) explaining what you will do and why, including alternatives.

## While You Write Code
- Add type hints (`mypy --strict`), docstrings, and tests for every new public function.
- Never put secrets in code, logs, prompts, or tests.
- Never bypass the Tool Gateway or approval flow.

## Before You Finish
- Update the affected module `README.md` files and the root `README.md` (files, functions, features).
- Update the decision record with files changed and final consequences.
- Run: `ruff check`, `mypy`, `pytest`, `import-linter`, `scripts/gen_module_index.py --check`.
