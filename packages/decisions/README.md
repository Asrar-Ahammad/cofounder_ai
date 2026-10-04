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
- `definitions/__init__.py`
- `definitions/approval_risk.py` (2 public symbols)
  - `build_approval_risk_question`: Construct Question for assessing tool execution risk.
  - `fail_closed_approval_risk`: Return fail-closed risk rating when model is unreachable or uncalibrated.
- `definitions/check_brand_voice_fit.py` (2 public symbols)
  - `build_check_brand_voice_fit_question`: Construct Question evaluating draft copy against brand voice and platform norms.
  - `fail_closed_check_brand_voice_fit`: Return fail-closed rating when brand voice evaluation is uncertain.
- `definitions/classify_founder_intent.py` (2 public symbols)
  - `build_founder_intent_question`: Construct Question to classify inbound founder message intent.
  - `fail_closed_founder_intent`: Return fail-safe intent when classifier is unavailable.
- `definitions/classify_outreach_reply.py` (2 public symbols)
  - `build_classify_outreach_reply_question`: Construct Question to classify the sentiment and intent of an outreach reply.
  - `fail_closed_classify_outreach_reply`: Return fail-closed classification when reply intent is ambiguous.
- `definitions/fan_out_event.py` (2 public symbols)
  - `build_event_fanout_question`: Construct Question to decide if an incoming domain event triggers immediate re-planning.
  - `fail_closed_event_fanout`: Return fail-safe option when event fan-out model is unavailable.
- `definitions/gate_legal_answer.py` (2 public symbols)
  - `build_gate_legal_question`: Construct Question for determining whether statutory grounding warrants answering or abstaining.
  - `fail_closed_gate_legal_answer`: Return fail-closed decision when legal retrieval confidence is uncertain.
- `definitions/judge_trace_quality.py` (2 public symbols)
  - `build_trace_quality_question`: Construct Question to evaluate the quality of an agent execution step.
  - `fail_closed_trace_quality`: Return fail-closed quality assessment when evaluator is down.
- `definitions/qualify_lead.py` (2 public symbols)
  - `build_qualify_lead_question`: Construct Question to qualify an inbound or outbound sales lead against the ICP.
  - `fail_closed_qualify_lead`: Return fail-closed rating when lead qualification is uncertain.
- `definitions/route_model_tier.py` (2 public symbols)
  - `build_model_tier_question`: Construct Question for choosing LLM tier based on task complexity and budget.
  - `fail_closed_model_tier`: Return fail-safe tier when decision model is unavailable.
- `definitions/route_supervisor.py` (2 public symbols)
  - `build_supervisor_routing_question`: Construct Question for routing next task to a specialist agent or human.
  - `fail_closed_supervisor_routing`: Return fail-closed route when supervisor decision is ambiguous or model is down.
- `definitions/screen_compliance.py` (2 public symbols)
  - `build_screen_compliance_question`: Construct Question for screening marketing or web copy for regulatory compliance.
  - `fail_closed_screen_compliance`: Return fail-closed risk rating when compliance screening is uncertain.
- `definitions/screen_untrusted_content.py` (2 public symbols)
  - `build_screening_question`: Construct Question for screening untrusted inbound text.
  - `fail_closed_content_screening`: Return fail-closed classification when screening model is unavailable.
- `definitions/select_context_to_keep.py` (2 public symbols)
  - `build_context_compaction_question`: Construct Question to decide context management strategy when approaching limit.
  - `fail_closed_context_compaction`: Return fallback compaction strategy.
- `definitions/tag_pain_point.py` (2 public symbols)
  - `build_pain_point_question`: Construct Question to extract customer pain point category from user reviews.
  - `fail_closed_pain_point`: Return fallback tag when decision model is unavailable.
- `definitions/triage_comment_or_dm.py` (2 public symbols)
  - `build_triage_comment_or_dm_question`: Construct Question for triaging incoming social comments or direct messages.
  - `fail_closed_triage_comment_or_dm`: Return fail-closed risk rating when message triage is uncertain.
- `definitions/triage_signal.py` (2 public symbols)
  - `build_signal_triage_question`: Construct Question to classify scraped signal into actionable category.
  - `fail_closed_signal_triage`: Return fail-safe classification for signal triage.
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
