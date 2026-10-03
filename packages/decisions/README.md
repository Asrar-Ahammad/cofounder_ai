# Decisions Package (`packages/decisions`)

**Purpose:** Implements the System One decision layer behind the `DecisionModel` port. Evaluates fast, typed, probabilistic decisions across 19 use cases (D1-D19).

## Files
- `ports.py` — Protocols and models: `Question`, `Decision`, and `DecisionModel`.

## Public Functions & Classes
- `Question`: Pydantic model for typed multi-choice queries (must contain 'other').
- `Decision`: Pydantic model for the selected option with calibrated probabilities.
- `DecisionModel`: Protocol for evaluating questions against typed states.

## Module Index
<!-- BEGIN GENERATED -->

### Files & Manifest

- `__init__.py`
- `adapters/jev_client.py` (1 public symbols)
  - `JevClient`: Adapter communicating with TypeSafe Jev hosted API.
- `definitions/approval_risk.py` (2 public symbols)
  - `build_approval_risk_question`: Construct Question for assessing tool execution risk.
  - `fail_closed_approval_risk`: Return fail-closed risk rating when model is unreachable or uncalibrated.
- `definitions/screen_untrusted_content.py` (2 public symbols)
  - `build_screening_question`: Construct Question for screening untrusted inbound text.
  - `fail_closed_content_screening`: Return fail-closed classification when screening model is unavailable.
- `policy/apply_threshold.py` (1 public symbols)
  - `apply_threshold`: Map decision choice and probabilities to an execution band.
- `policy/hard_rules.py` (2 public symbols)
  - `is_never_auto`: Check whether an action is prohibited from auto-approval.
  - `is_fail_closed`: Check whether a decision use-case must fail closed.
- `ports.py` (3 public symbols)
  - `Question`: A typed question presented to a System One decision model.
  - `Decision`: The outcome of a single question evaluated by the System One model.
  - `DecisionModel`: Protocol for System One decision model providers.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/decisions
```
