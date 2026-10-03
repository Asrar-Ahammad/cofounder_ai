# 0007: Phase 3 Go to Market, Social & Sales Agents, and Suppression Infrastructure

## Context
Phase 1 and Phase 2 delivered the Core Intelligence Engine (orchestration, market research, validation, financial scenarios) and Regulatory Guardrails (legal RAG, D11/D12 screening, HTML sanitization, sandboxed web preview).
Phase 3 expands autonomous operations into customer acquisition and go-to-market:
1. **Marketing & Social Agent (`packages/agents/marketing/`)**: Multi-platform social content generation (X, LinkedIn, Meta via Ayrshare), brand voice fit evaluation (System One Decision D14), and scheduled content calendar staging with founder approval gates.
2. **Sales Agent & CRM (`packages/agents/sales/`)**: Inbound/outbound prospect lead qualification (Decision D15), personalized outreach drafting, prospect reply classification (Decision D16), and calendar booking integration (Cal.com).
3. **Immediate Unsubscribe Suppression**: Automatic, atomic insertion into `suppression_list` upon `unsubscribe` reply classification; hard code-level blocking in `ToolGateway` preventing any outbound communications to suppressed contacts without human override.
4. **Inbound Comment/DM Triage & Crisis Alerting**: Evaluating incoming public social interactions and DMs (Decision D13) into spam, lead, complaint, question, or crisis. When classified as `crisis`, automated bot responses are strictly blocked and urgent alerts escalate to the founder.
5. **Customer OAuth KMS Envelope Encryption (`packages/security/crypto.py`)**: Hardware-grade envelope encryption with per-tenant encryption context, guaranteeing external tokens (Gmail, Ayrshare/Meta) are encrypted at rest and never exposed to logs, traces, or model context.

## Decisions
1. **System One Decision Models (D13–D16):**
   - **D13 (`triage_comment_or_dm`)**: Classes: `spam | lead | complaint | question | crisis`. Fallback defaults to `crisis` (fail-closed, alerts founder).
   - **D14 (`check_brand_voice_fit`)**: Classes: `pass | revise`. Fallback defaults to `revise` (fail-closed, prevents off-brand posts).
   - **D15 (`qualify_lead`)**: Classes: `nurture | book_call | disqualify`. Fallback defaults to `nurture`.
   - **D16 (`classify_outreach_reply`)**: Classes: `interested | objection | not_now | out_of_office | unsubscribe | other`. Fallback defaults to `other`.
2. **Strict Layer Independence:**
   - Marketing and Sales agents are compiled LangGraph subgraphs under `packages/agents/`.
   - They communicate exclusively through the Shared Brain, domain events, and state dictionaries, never importing across agent boundaries.
3. **KMS Token Protection & In-Memory Lifecycle:**
   - External OAuth tokens are encrypted using AES-256-GCM / Fernet with key derivation bound to tenant identity (`tenant_id`). Plaintext credentials reside only in transient memory during adapter execution.
4. **Zero-Tolerance Suppression Choke-Point:**
   - If an inbound message is classified as `unsubscribe` by D16 or contains canonical opt-out cues ("unsubscribe", "stop", "opt out"), the recipient is immediately registered in the tenant's suppression list.
   - The `ToolGateway` checks the suppression registry on every email/outreach execution and raises `PolicyViolation` if a recipient is suppressed.
5. **Ports and Adapters Pattern:**
   - Integrations depend on abstract protocols in `packages/integrations/ports.py` (`SocialPublisher`, `EmailSender`, `CalendarScheduler`).
   - Concrete adapters (`ayrshare.py`, `gmail.py`, `calcom.py`) implement these protocols without leaking third-party SDK dependencies into agent logic.

## Consequences
- Enables automated, safe customer acquisition campaigns while eliminating compliance liabilities (CAN-SPAM/GDPR unsubscribe violations, brand voice degradation, PR crises).
- Maintains strict monorepo layer boundaries and 100% test coverage across all new public symbols.
