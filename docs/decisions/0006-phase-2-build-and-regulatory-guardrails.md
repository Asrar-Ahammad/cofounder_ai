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
   - Legal documents are chunked along statutory section boundaries preserving act title, enactment year, section number, and authoritative government URL.
   - Layer rules strictly maintained: `packages/rag` depends only on `packages/core`.
2. **Mandatory Abstention Gate (D11):**
   - Out-of-corpus, ambiguous, or low-scoring statutory queries trigger an explicit abstention (`abstain`) rather than hallucinating legal advice, accompanied by a standard legal counsel disclaimer.
3. **Defense-in-Depth HTML Sanitization in `packages/agents/web/`:**
   - Generated landing page HTML is sanitized with regex-based tag and attribute strippers removing `<script>`, `javascript:`, data URIs, and inline `on*` event handlers before deployment.
   - Content is screened through Decision D12 (`screen_compliance`) before deployment to prevent deceptive or regulated marketing claims.
4. **Sandboxed Preview Deployment:**
   - Web agent deploys to isolated sandbox domains (simulated S3/CloudFront) with founder approval hooks.
5. **Deterministic Scenario Simulation:**
   - Financial scenarios (best, base, worst) execute pure Monte-Carlo/variance logic without calling external APIs or mutable databases.

## Consequences
- Guarantees compliance safety: zero hallucinated legal statutes and zero unscreened marketing claims published to the public.
- Preserves layer independence and enables automated evaluation of regulatory accuracy and web generation.
