# 0006: Phase 2 Build and Regulatory Guardrails

## Context
Phase 1 established the Core Intelligence Engine (Supervisor Orchestrator, Market Intelligence, Validation, Financial modeling, and System One decisions D3–D10).
Phase 2 builds the regulatory guardrails and prototype execution infrastructure:
1. **Legal & Compliance RAG Engine**: Mandatory citation or abstention over official statutes and gazettes (e.g. India DPDP Act 2023, Companies Act 2013, Delaware General Corporation Law).
2. **System One Decision D11 (`gate_legal_answer`)**: Strictly abstains from answering if statutory retrieval confidence or citation grounding is below safety threshold.
3. **System One Decision D12 (`screen_compliance`)**: Screens landing page copy, marketing claims, and public disclosures for regulated claims or missing consent.
4. **Web Agent Subgraph (`packages/agents/web/`)**: Generates MVP single-page landing pages with Tailwind CSS, sanitized HTML (script/event-handler stripping), compliance pre-screening, and deployment to an isolated sandbox domain.
5. **Multi-Scenario Simulation Engine**: Computes best-case, base-case, and worst-case runway and cash flow projections while highlighting blind spots with side-effect tools disabled.

## Decisions
1. **Statutory Hierarchy Chunking in `packages/rag/`:**
   - Legal documents are chunked along statutory section and article boundaries preserving act title, enactment year, section/article number, section type, and authoritative government URL.
   - Default corpus indexes DPDP Act 2023, Companies Act 2013, Delaware General Corporation Law (DGCL), and GDPR.
   - Layer rules strictly maintained: `packages/rag` depends only on `packages/core`.
2. **Mandatory Abstention & Clarification Gate (D11):**
   - Completely out-of-corpus queries (score < 0.20) trigger an explicit abstention (`abstain`) rather than hallucinating legal advice, accompanied by a standard legal counsel disclaimer.
   - Borderline or ambiguous queries (0.20 <= score < 0.35) trigger a request for clarification (`clarify`) prompting for specific jurisdiction or statute details.
   - Highly confident matches (score >= 0.35) require verified statutory section citations with authoritative `https://` URLs before answering.
3. **Defense-in-Depth HTML Sanitization in `packages/agents/web/`:**
   - User inputs in landing page templates are escaped with `html.escape()`. Styles use stylesheet `<link>` tags rather than executable `<script>` tags.
   - Generated landing page HTML is sanitized with regex-based tag and attribute strippers removing `<script>`, `<iframe>`, `javascript:`, `data:` URIs, and inline `on*` event handlers before deployment.
   - Content is screened through Decision D12 (`screen_compliance`) before deployment to prevent deceptive or regulated marketing claims and unconsented data collection.
4. **Sandboxed Preview Deployment with Founder Approval:**
   - Web agent deploys to isolated sandbox domains with strict gating: requires both `compliance_status == "clean"` and explicit founder review (`needs_approval == False`). If awaiting approval or flagged, deployment remains halted/staged.
5. **Deterministic Multi-Scenario Financial Modeling:**
   - Pure sensitivity and variance modeling computes best, base, and worst-case scenarios without external I/O or mutable state.
   - Exact break-even unit volumes use mathematical ceiling rounding (`math.ceil`).
   - Dynamically models COGS variance, monthly customer churn rates, and runway duration across all scenarios.

## Consequences
- Guarantees compliance safety: zero hallucinated legal statutes and zero unscreened marketing claims published to the public.
- Ensures landing page deployment requires explicit founder sign-off before public accessibility.
- Preserves layer independence and enables automated evaluation of regulatory accuracy and web generation.
