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
- `financial/agent.py` (1 public symbols)
  - `FinancialAgent`: Specialist agent modeling unit economics, pricing, and spend boundaries.
- `financial/build_graph.py` (1 public symbols)
  - `build_financial_graph`: Construct and compile the Financial LangGraph execution pipeline.
- `financial/model_unit_economics.py` (1 public symbols)
  - `calculate_unit_economics`: Calculate margins, LTV, CAC payback, and break-even targets.
- `financial/simulate_scenarios.py` (1 public symbols)
  - `simulate_financial_scenarios`: Generate best-case, base-case, and worst-case runway and unit economics scenarios.
- `financial/state.py` (2 public symbols)
  - `UnitEconomicsMetrics`: Calculated unit economics and runway projections.
  - `FinancialState`: State passing through the Financial LangGraph subgraph.
- `financial/write_constraints.py` (1 public symbols)
  - `formulate_constraint_limits`: Derive versioned venture constraint limits from financial models.
- `legal/__init__.py`
- `legal/agent.py` (1 public symbols)
  - `LegalAgent`: Specialist agent for statutory compliance, regulatory RAG, and mandatory citation gating.
- `legal/evaluate_regulatory_gate.py` (1 public symbols)
  - `evaluate_statutory_grounding`: Evaluate retrieval grounding and citation validity to answer, clarify, or abstain.
- `legal/retrieve_statutes.py` (1 public symbols)
  - `retrieve_relevant_statutes`: Retrieve authoritative statutory sections matching the legal query and jurisdiction.
- `legal/state.py` (1 public symbols)
  - `LegalState`: State passing through the Legal and Compliance LangGraph subgraph.
- `legal/synthesize_legal_memo.py` (1 public symbols)
  - `synthesize_legal_memorandum`: Generate structured statutory memorandum with explicit section/article citations.
- `market_intel/__init__.py`
- `market_intel/agent.py` (1 public symbols)
  - `MarketIntelAgent`: Specialist agent tracking live market trends, competitors, and sentiment.
- `market_intel/analyze_competitors.py` (1 public symbols)
  - `extract_competitor_profiles`: Extract competitor landscape from search results and signals.
- `market_intel/build_graph.py` (1 public symbols)
  - `build_market_intel_graph`: Construct and compile the Market Intelligence LangGraph execution pipeline.
- `market_intel/extract_pain_points.py` (1 public symbols)
  - `extract_customer_pain_points`: Extract actionable customer pain points and feature gaps.
- `market_intel/state.py` (3 public symbols)
  - `CompetitorProfile`: Structured competitor insight extracted from market intelligence.
  - `MarketSignal`: Categorized market signal from live search or web scrape.
  - `MarketIntelState`: State passing through the Market Intelligence LangGraph subgraph.
- `market_intel/triage_signal.py` (1 public symbols)
  - `triage_raw_signals`: Triage raw search snippets into categorized market signals.
- `marketing/__init__.py`
- `operations/__init__.py`
- `orchestrator/__init__.py`
- `orchestrator/agent.py` (1 public symbols)
  - `OrchestratorAgent`: Supervisor agent coordinating specialist agents across venture milestones.
- `orchestrator/build_graph.py` (1 public symbols)
  - `build_orchestrator_graph`: Construct and compile the master Orchestrator Supervisor graph.
- `orchestrator/model_milestones.py` (3 public symbols)
  - `initialize_default_milestones`: Initialize standard venture milestones if none exist.
  - `update_milestone_progress`: Update progress for a specific milestone.
  - `evaluate_stage_progress`: Evaluate milestone progress to advance or align the venture stage.
- `orchestrator/route_tasks.py` (1 public symbols)
  - `route_next_venture_task`: Determine the next specialist agent to activate based on milestone progress.
- `orchestrator/state.py` (2 public symbols)
  - `Milestone`: Venture milestone tracking progress toward the north-star goal.
  - `OrchestratorState`: Master state passing through the Orchestrator Supervisor.
- `sales/__init__.py`
- `support/__init__.py`
- `validation/__init__.py`
- `validation/agent.py` (1 public symbols)
  - `ValidationAgent`: Specialist agent calculating TAM/SAM/SOM and Go/No-Go feasibility.
- `validation/build_graph.py` (1 public symbols)
  - `build_validation_graph`: Construct and compile the Validation LangGraph execution pipeline.
- `validation/market_sizing.py` (1 public symbols)
  - `calculate_market_sizing`: Calculate TAM, SAM, and SOM using transparent top-down and bottom-up formulas.
- `validation/scoring/__init__.py`
- `validation/scoring/problem_severity.py` (1 public symbols)
  - `calculate_problem_severity`: Evaluate customer problem severity with citation-backed evidence.
- `validation/scoring/timing_score.py` (1 public symbols)
  - `calculate_timing_score`: Calculate venture market timing score based on trends and technology tailwinds.
- `validation/state.py` (3 public symbols)
  - `ScoreResult`: Rubric score with transparent evidence citations.
  - `MarketSizeResult`: Calculated TAM, SAM, and SOM figures with formula explanation.
  - `ValidationState`: State passing through the Validation LangGraph subgraph.
- `validation/synthesize_report.py` (1 public symbols)
  - `synthesize_validation_report`: Synthesize final validation evaluation and recommendation.
- `web/__init__.py`
- `web/agent.py` (1 public symbols)
  - `WebAgent`: Specialist agent generating sanitized landing page prototypes and preview deployments.
- `web/deploy_sandbox.py` (1 public symbols)
  - `deploy_to_sandbox_environment`: Deploy sanitized landing page to isolated tenant sandbox domain.
- `web/generate_landing_page.py` (1 public symbols)
  - `generate_landing_page_html`: Generate responsive MVP landing page HTML with stylesheet styling and escaped inputs.
- `web/sanitize_html.py` (1 public symbols)
  - `sanitize_landing_page_html`: Sanitize generated landing page HTML by stripping executable scripts, handlers, and data URIs.
- `web/screen_web_content.py` (1 public symbols)
  - `screen_landing_page_compliance`: Screen landing page copy for regulatory claims, missing disclosures, and consent issues.
- `web/state.py` (1 public symbols)
  - `WebAgentState`: State passing through the Web Agent LangGraph subgraph.

<!-- END GENERATED -->

## Testing
```bash
pytest tests/unit/agents
```
