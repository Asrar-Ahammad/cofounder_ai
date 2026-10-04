# 0008: Phase 4 Autonomous Inbound Operations, Webhooks, and Support Agent

## Context
Phases 0 through 3 established the monorepo foundation, intelligence engines (orchestrator, market intel, validation, financials), build tools (regulatory RAG, web sandboxing), and outbound acquisition (marketing, sales, suppression, and token envelope encryption).
Phase 4 expands autonomous operations into customer-facing inbound communications:
1. **Dedicated Webhook Receiver (`apps/webhooks/`)**: An isolated, minimal FastAPI deployable accepting webhooks from external channels (Meta/WhatsApp, Stripe) with strict cryptographic signature verification and zero-latency enqueueing into Redis Streams (`incoming_webhooks`).
2. **Support & Reception Agent (`packages/agents/support/`)**: A compiled LangGraph subgraph that handles incoming customer queries across Web chat and WhatsApp, classifies intent, checks frustration/churn risk, answers from approved venture knowledge, or escalates to the founder.
3. **Inbound Routing & Frustration Decisions (D17 & D18)**:
   - **D17 (`route_inbound_message`)**: Classifies inbound customer messages into `answer_from_kb`, `book_meeting`, `escalate`, or `spam`.
   - **D18 (`detect_frustration`)**: Evaluates customer sentiment into `calm`, `frustrated`, or `urgent_risk`. Any detected frustration immediately bypasses automated answering and routes to human founder escalation.
4. **Grounded Knowledge Base Q&A**: Customer answers are strictly constrained to venture-approved facts and documents with citation grounding, abstaining and escalating if information is absent.
5. **Two-Way Messaging Port & WhatsApp Adapter (`packages/integrations/adapters/whatsapp.py`)**: Abstract protocol `InstantMessenger` allowing customer communications via official WhatsApp Business Cloud API with egress filtering and non-blocking I/O.

## Decisions
1. **System One Decision Models (D17 & D18):**
   - **D17 (`route_inbound_message`)**: Options: `answer_from_kb | book_meeting | escalate | spam`. Fail-closed fallback defaults to `escalate`.
   - **D18 (`detect_frustration`)**: Options: `calm | frustrated | urgent_risk`. Fail-closed fallback defaults to `frustrated`.
2. **Isolated Webhook Architecture:**
   - `apps/webhooks/main.py` is decoupled from background agent execution.
   - It validates HMAC-SHA256 signatures in constant time (`hmac.compare_digest`):
     - Meta `X-Hub-Signature-256`.
     - Stripe `stripe-signature` timestamp and signature.
   - Validated payloads are immediately acknowledged with HTTP 200 and published to Redis Streams `incoming_webhooks` for asynchronous worker processing.
3. **Frustration-First Customer Triage:**
   - In the Support Agent graph, `detect_frustration` is evaluated before any automated resolution or knowledge retrieval.
   - If frustration or urgent risk is detected, the agent immediately halts automated text generation, creates a high-priority escalation alert, and notifies the founder.
4. **Strict Grounded Q&A Guardrails:**
   - The knowledge base answering node requires approved factual context. If query context is ungrounded or ambiguous, the node abstains from making commitments or promises and escalates to human review.
5. **Decoupled Messaging Port:**
   - Support Agent communicates through `InstantMessenger` protocol in `packages/integrations/ports.py`.
   - `WhatsAppCloudAdapter` provides production Meta Graph API calls and simulation mode for local development.

## Consequences
- Enables 24/7 autonomous customer inbound support while eliminating hallucination and brand risk through strict KB grounding and fail-safe frustration escalation.
- Secures external webhook ingestion against forged signatures and DDoS slowdowns by immediate queueing into Redis Streams.
- Maintains strict layer boundaries: `apps/webhooks` depends on `core`, `agents/support` communicates through events and Shared Brain.

### Files Changed
- `apps/webhooks/main.py`: Isolated FastAPI webhook receiver with Meta and Stripe cryptographic verification.
- `apps/webhooks/README.md`: Updated module documentation with generated index.
- `packages/integrations/ports.py`: Added `InstantMessenger` abstract protocol.
- `packages/integrations/adapters/whatsapp.py`: Meta Graph WhatsApp Cloud API adapter with egress validation.
- `packages/decisions/definitions/route_inbound_message.py`: Decision D17 for intent routing.
- `packages/decisions/definitions/detect_frustration.py`: Decision D18 for frustration and churn risk detection.
- `packages/agents/support/__init__.py`: Support agent package exports.
- `packages/agents/support/state.py`: SupportState model.
- `packages/agents/support/detect_sentiment.py`: Frustration and churn risk evaluation node.
- `packages/agents/support/route_intent.py`: Inbound customer intent classification node.
- `packages/agents/support/answer_grounded.py`: Grounded KB Q&A node with citation enforcement.
- `packages/agents/support/escalate_ticket.py`: Founder escalation and holding response node.
- `packages/agents/support/format_reply.py`: Response synthesis and calendar link formatting node.
- `packages/agents/support/agent.py`: Support Agent compiled LangGraph subgraph.
- `tests/unit/agents/test_support_agent.py`: End-to-end tests for Support Agent.
- `tests/unit/integrations/test_whatsapp_adapter.py`: Unit tests for WhatsApp Cloud adapter.
- `tests/unit/webhooks/test_webhook_receiver.py`: Signature and challenge verification tests.
- `tests/unit/decisions/test_phase4_decisions.py`: D17 & D18 validation tests.

