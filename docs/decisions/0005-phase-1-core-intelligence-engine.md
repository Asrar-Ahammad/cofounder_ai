# 0005: Phase 1 Core Intelligence Engine

## Context
Phase 0 established foundational substrates (multi-tenant Postgres RLS, Redis Streams event bus, Shared Brain, Tool Gateway with bounded idempotency, Approval Service, System One substrate D1-D2, and Next.js frontend).
Phase 1 implements the Core Intelligence Engine:
1. The Supervisor Orchestrator graph with milestone tracking and structured routing.
2. The Market Intelligence Agent (signals, competitor extraction, pain point tagging).
3. The Validation Agent (TAM/SAM/SOM, timing & severity rubric scoring with direct citations).
4. The Financial Agent (unit economics, break-even runway calculations, and hard constraint validation guards).
5. System One probabilistic decisions D3 through D10.
6. Integration ports for search & scraping (Tavily, Firecrawl).

## Decisions
1. **LangGraph Multi-Agent Architecture:**
   - The Orchestrator is a supervisor `StateGraph`. Specialist agents are compiled subgraphs.
   - Agents never import each other; they communicate strictly through the Shared Brain and Redis Streams domain events.
2. **Ports and Adapters:**
   - Search and scraping interfaces defined in `packages/integrations/ports.py` (`SearchClient`, `ScraperClient`).
   - Mock and concrete adapters in `packages/integrations/adapters/` adhering to ports without vendor leak.
3. **Hard Constraint Enforcement:**
   - Financial constraints (`budget_cap`, `max_cac`, `outreach_cap`) enforced in pure Python guards in `packages/core/constraints.py`.
4. **Transparent Rubric Scoring:**
   - Validation scoring rubrics in `packages/agents/validation/scoring/` require verifiable citation links for every score factor.

## Consequences
Establishes autonomous market research, validation, and financial modeling capability for early-stage ventures while maintaining layer isolation and testability.

### Code Review Hardening (PR #2)
1. **Mathematical Precision:** Unit economics `break_even_customers` uses `math.ceil` to ensure fractional customer requirements round up to solvency.
2. **Signal Classification:** Market intelligence signal regex uses strict word boundary matching `\b(sec|gdpr|fssai|regulation|compliance|law|statute)\b` to eliminate false positives on terms like "security".
3. **State Integrity:** Milestone reopening clears stale `completed_at` timestamps; `evaluate_stage_progress` dynamically synchronizes venture stage with milestone progress.
4. **Boundary Validation:** `ConstraintLimits` is frozen/immutable; `monthly_budget_cap` requires non-negative values; validation market sizing bounds customer count and percentages.
5. **Truth in Evidence:** Empty validation evidence leaves `evidence_refs` empty and explicitly marks citations as unverified/pending, preventing fabricated default links.
6. **Egress & Scraper Security:** Firecrawl scraper prevents remote SSRF via strict domain qualification and forbidden non-web ports, and raises `ExternalServiceError` on unconfigured credentials instead of generating fake pages.

