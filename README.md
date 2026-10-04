# Cofunder

AI startup co-founder suite: a supervisor-led swarm of specialist agents (LangGraph) sharing one persistent business brain, gated by human approvals and traced with LangSmith.

---

## Project Map

```
cofunder/
├── apps/
│   ├── api/                      # FastAPI entrypoint (REST & SSE streaming)
│   ├── worker/                   # Arq background queue consumers and schedulers
│   ├── webhooks/                 # Isolated inbound webhook receiver (Meta, Stripe)
│   └── web/                      # Next.js 15 (App Router) + React 19 + Tailwind CSS 4 (Inter font)
├── packages/
│   ├── core/                     # Domain models, events, errors, DB engine, config (pure, no external I/O)
│   ├── brain/                    # Shared Brain service, repositories, LangGraph checkpointer
│   ├── agents/                   # Specialist agent subgraphs (orchestrator, market intel, legal, etc.)
│   ├── tools/                    # Tool definitions, registry, allowlist and Tool Gateway
│   ├── integrations/             # External adapters (ports & adapters pattern)
│   ├── rag/                      # Ingest, chunking, pgvector retriever, citation verification
│   ├── approvals/                # Human-in-the-loop approval service & policies
│   ├── security/                 # Authz, KMS token encryption, SSRF protection, prompt injection shields
│   ├── decisions/                # System One decision layer (TypeSafe Jev + fallbacks, D1-D19)
│   └── observability/            # Logging, OpenTelemetry tracing, LangSmith setup
├── evals/                        # LangSmith benchmark datasets and evaluation suites
├── docs/                         # Architecture, data models, event catalog, decision records (ADRs)
├── scripts/                      # Utility and verification scripts (e.g. gen_module_index.py)
├── infra/                        # Docker, Terraform, Kubernetes definitions
├── tests/                        # Unit, contract, integration, and security test suites
├── AGENTS.md                     # Agent engineering rules & coding standards
└── pyproject.toml                # Dependencies, ruff, mypy, pytest, and import-linter configs
```

---

## Architectural Principles

1. **Modular monolith first:** Strict layer separation enforced by `import-linter`.
2. **Ports and adapters:** Pure business logic depends on interfaces (`packages/integrations/ports.py`), never vendor SDKs.
3. **Subgraphs with typed contracts:** Every agent exposes typed inputs, outputs, allowed tools, and domain events.
4. **State is data, not prose:** Constraints (budget, CAC, outreach volume) are versioned records in Postgres.
5. **Deny by default:** Tools, tenant access, network egress, and permissions start closed.
6. **Everything observable:** Full trace coverage in LangSmith and OpenTelemetry.
7. **Idempotent side effects:** Every outbound action carries a deterministic idempotency key.
8. **Right model for the job:** System One models (Jev) make fast probabilistic decisions; Claude 3.5 Sonnet handles reasoning and writing; plain Python code enforces hard constraints.

---

## Getting Started

### Prerequisites
- Python 3.12+
- `uv` package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Docker & Docker Compose (for PostgreSQL + pgvector and Redis)
- Node.js 22 LTS (for Next.js frontend)

### Setup Virtual Environment
```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Local Services
```bash
docker compose up -d
```

### Running Checks & Tests
```bash
# Code formatting & linting
ruff check .
ruff format --check .

# Static type checking
mypy packages

# Layer rule verification
lint-imports

# Unit & integration tests
pytest

# Verify living documentation
python scripts/gen_module_index.py --check
```

---

## Project Roadmap & Status

- **Phase 0: Foundations & Substrate (Complete):** Monorepo architecture, Postgres RLS, Redis Streams event bus, Shared Brain, Tool Gateway with bounded idempotency, Approval Service, System One substrate (D1, D2), Next.js 15 UI shell.
- **Phase 1: Core Intelligence Engine (Complete):** Orchestrator Supervisor graph with milestone tracking, Market Intelligence Agent with signal triage, Validation Agent with TAM/SAM/SOM and citation-backed rubrics, Financial Agent with unit economics & hard constraint code guards, System One Decisions D3–D10, and search/scraper adapters.
- **Phase 4: Autonomous Inbound & Customer Operations (Complete):** Dedicated webhook receiver deployable (`apps/webhooks`) with Meta `X-Hub-Signature-256` and Stripe signature verification, Support & Reception Agent (WhatsApp Cloud API / Web), System One Inbound Routing (D17) and Frustration/Churn Detection (D18), grounded KB Q&A with strict citations, and fail-safe founder escalation loops.
- **Phase 5: Scale, Enterprise Readiness & Model Migration (Upcoming):** Operations & Inventory Agent (D19), System One open-source model migration (SemIf/Kev canary cutover), Twilio Voice, multi-region data residency (India DPDP & GDPR), and SOC 2 Type 1 evidence automation.

---

## Environment Variables (.env)
A `.env.example` file is provided in the repository root. Required keys include:
- `DATABASE_URL`: PostgreSQL connection string (asyncpg / psycopg3)
- `REDIS_URL`: Redis connection string
- `CLERK_SECRET_KEY`: Clerk authentication secret
- `AWS_KMS_KEY_ID`: KMS key ID for customer OAuth token envelope encryption
- `LANGSMITH_API_KEY`: LangSmith tracing key
- `ANTHROPIC_API_KEY`: Anthropic Claude API key
- `JEV_API_KEY`: TypeSafe Jev API key
- `TAVILY_API_KEY`: Tavily web search API key
- `FIRECRAWL_API_KEY`: Firecrawl web scraper API key

