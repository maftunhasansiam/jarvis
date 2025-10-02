### canonical milestone plan for the Jarvis project

Purpose: This file is the single source-of-truth for the Jarvis / AnythingLLM integration project. Put it in the repository root as PROJECT_MILESTONES.md. All ChatGPT sessions and contributors must reference and update this file when milestones progress.

### How to use this file

Read the entire plan before starting work. This file encodes scope, safety gates, and the commit/PR style we follow.

When a milestone (or part of it) is completed, update the Changelog section at the bottom with the status and a short note, and commit the change.

Follow the Persona Rules and the one-task-one-commit discipline described below.

### Guiding Principles (Persona rules)

Minimal & pragmatic: Implement the smallest thing that moves the project forward.

Safety first: Tools and features that touch system, filesystem, finances, or IoT are requires_approval: true by default. Local system control must go through the Local Agent (M5) and explicit user opt-in.

One task → one commit/PR: Each logical unit is a separate commit/PR with tests and run steps.

Testable: Unit tests and minimal integration tests for each milestone.

Least-privilege: Tools default to no network/filesystem/system access unless explicitly allowed by manifest and approval.

Human-in-the-loop: UI approval controls for sensitive operations.

Auditability: All sensitive actions must be logged with immutable audit records.






### High-level milestone list (final)

M0 — Repo Prep & Developer Environment

M1 — Agent Core & Planner (Minimal Autonomous Loop)

M2 — Tool Registry, Manifests & Sandboxed Runners

M3 — Memory (short & long-term) + Embeddings

M4 — Workflow Orchestration, Scheduler & Reactive Engine

M5 — Local Agent (OS control) + IoT Integration

M6 — UI Dashboard & Human-in-the-loop

M7 — Safety, Policy Engine, Audit & Monitoring

M8 — Domain Connectors & Personalization

M9 — Creative & Research Assistant + Production Hardening


Note: M1 scaffolding has been implemented in this project as safe, in-memory components. The checkmark above indicates M1 scaffold completion; remaining M1 deliverables (persistent DB & full LLM integration) are tracked in M3 and M2 respectively.











### Milestones (detailed)


# M0 — Repo Prep & Developer Environment

## Goal: Prepare a reproducible developer environment so different sessions/people can work in parallel.

Deliverables:

- Monorepo skeleton (packages/), docker-compose dev stack, devcontainer, CI skeleton.

- Linting, pre-commit hooks, README/ARCHITECTURE.

- Minimal “example run” instructions.

### Files to add/update:-

/README.md
/ARCHITECTURE.md
/docker-compose.yml        # postgres, redis, minio, api (dev), ui (dev)
/.devcontainer/devcontainer.json
/.github/workflows/ci.yml  # lint + tests skeleton
/pre-commit-config.yaml
/packages/api/pyproject.toml
/packages/ui/package.json


### Tech choices

- Python FastAPI for Agent Core (interop-friendly).

- Node/React (Vite or Next) for UI.

- Postgres (production), SQLite allowed for dev.

- Redis for queues.

### Persona constraints

- Only add infra needed for local dev. No cloud deployment code yet.

- Each infra item is a separate commit.

### Acceptance

- docker-compose up brings dev services up (API returns {"msg":"ok"}).

- CI runs linter & unit tests (empty test suite at first).








# M1 — Agent Core & Planner (Minimal Autonomous Loop) — IMPLEMENT FIRST

## Goal: Minimal working agent: accept a goal, produce a plan (stub/LLM), execute safe tools, log results (initially in-memory).

Why it’s first: This is the agent’s “brain.” Everything else plugs into it.

### Deliverables

- FastAPI service: /v1/agent/plan, /v1/agent/execute, /v1/agent/status.

- Planner stub (safe hardcoded behaviors at first; optionally an adapter to AnythingLLM).

- Executor that runs only echo and http_request tools.

- Tool Base interface.

- In-memory task & log store (persistence deferred until M3).

- Unit tests and curl examples.

### Files (scaffold)

/packages/api/app/main.py
/packages/api/app/routes/agent.py
/packages/api/app/agent/planner.py
/packages/api/app/agent/core.py
/packages/api/app/agent/executor.py
/packages/api/app/agent/tools/__init__.py
/packages/api/app/agent/tools/echo_tool.py
/packages/api/app/agent/tools/http_tool.py
/packages/api/app/models/agent_models.py
/tests/test_agent.py


### Key models / schemas (Pydantic)

PlanRequest(goal: str, context: dict)
PlanStep(id: str, action: str, input: dict, requires_approval: bool=False)
PlanResponse(task_id: UUID, steps: List[PlanStep])
ExecutionResult(step_id: str, status: str, output: dict)


### Planner

M1: safe stub with a predictable mapping (e.g. if "fetch" in goal -> http_request).

Also include an LLM adapter skeleton (llm_adapter.py) so LLM can be enabled later.

### Executor

Validate step against Tool manifest (exists + input schema).

No arbitrary shell exec. No filesystem access.

Return structured outputs: {status, output, metadata}.

### Logging

In-memory tasks and task_logs dicts, with functions get_task, save_task, append_log.

### Acceptance

POST /v1/agent/plan -> returns JSON steps for simple goals.

POST /v1/agent/execute -> runs steps and returns results.

pytest unit tests for planner mapping and executor tool responses.

### Persona enforcement

Tools = echo, http_request only. Any addition requires explicit approval.

Planner uses stub by default; enable LLM only after safety checks (M2).

### Commit plan (one commit per unit)

- chore(m1): add pydantic models and tests

- feat(m1): add echo tool

- feat(m1): add http_request tool

- feat(m1): implement planner stub

- feat(m1): implement executor

- feat(m1): add agent routes + main entrypoint

- test(m1): add unit tests + run steps in README











# M2 — Tool Registry, Manifests & Sandboxed Runners

Goal: Make tools pluggable, discoverable, validated, permissioned, and sandboxed.

Deliverables

Tool manifest format (JSON Schema / YAML) and loader.

BaseTool interface & tool metadata registry.

Per-tool permissions metadata: {network, filesystem, system, external_api}.

Local sandbox runner (first iteration: process isolation + Python restricted runner; next: run each tool in its own Docker container).

Tool versioning & manifest discovery.

Files

/packages/api/app/tools/base.py
/packages/api/app/tools/registry.py
/packages/api/app/tools/manifests/*.yaml
/packages/api/app/tools/runners/docker_runner.py
/packages/api/app/security/permissions.py


Tool manifest (example)

name: http_request
version: "0.1.0"
inputs:
  url: {type: string, required: true}
outputs:
  status_code: int
  body: string
permissions:
  network: true
  filesystem: false
  system: false
sandbox: docker


Behavior

Agents ask registry for tool list; executor resolves tool via registry metadata.

Registry enforces input schema before execution.

Tools that request filesystem/system require an approval gate.

Safety

Default manifest for custom tools disallows network/filesystem until explicitly allowed.

Adding a tool that requests system or filesystem triggers a “manual review required” flag.

Acceptance

Drop a manifest + module; registry loads it.

Executor executes registered tools via runner and respects permissions.

Commit plan

feat(m2): add tool base class

feat(m2): add tool registry + manifest loader

feat(m2): add docker_runner scaffold

test(m2): add registry unit tests

M3 — Memory (short-term & long-term) + Embeddings

Goal: Add persistence for tasks & logs; add semantic memory (vector search) to support contextual planning and personalization.

Deliverables

Postgres migrations: agents, tasks, task_logs, memories.

Memory storage layer: pgvector (or plugin for Weaviate/Milvus) via an abstraction.

Embeddings wrapper (LLM embeddings or 3rd-party) with fallbacks.

Memory API: /v1/memory/add, /v1/memory/query.

Integrate memory retrieval into planner pipeline.

Files

/migrations/0001_init.sql
/migrations/0002_memories.sql
/packages/api/app/db/*.py   # db connection + helpers
/packages/api/app/memory/storage.py
/packages/api/app/memory/embeddings.py
/packages/api/app/routes/memory.py


DB schemas

CREATE TABLE tasks (...);
CREATE TABLE task_logs (...);
CREATE TABLE memories (
  id uuid PRIMARY KEY,
  agent_id uuid,
  type text check(...),
  content text,
  embedding vector(1536),
  metadata jsonb,
  created_at timestamp default now()
);


Behavior

Planner asks memory for relevant context and appends top-N items to prompt.

Memory organizer categorizes items as ephemeral, episodic, semantic.

Persona

Start with pgvector (Postgres + pgvector extension). If user wants heavier vector store later, we can swap via abstraction layer.

Sensitive memories require opt-in; default is not to store personal credentials.

Acceptance

Add memory entry and query similar items.

Planner uses memory to enrich a plan (unit test: planner includes memory content when present).

Commit plan

feat(m3): add db layer + migrations

feat(m3): add memory storage + embeddings abstraction

test(m3): memory query unit tests

M4 — Workflow Orchestration, Scheduler & Reactive Engine

Goal: Durable multi-step workflows with retries, branching, and reactive exception handling.

Deliverables

Orchestrator service (state machine): workflow definitions, step state transitions.

Worker pool using Celery + Redis or RQ. (Celery recommended.)

Scheduler (Celery Beat or APScheduler).

Event Bus (Redis pub/sub) for triggers.

Workflow API: create/update workflows, run, pause, resume.

Reactive rules engine: retry on errors, conditional branching, alerts.

Files

/packages/api/app/orchestrator/orchestrator.py
/packages/api/app/orchestrator/models.py
/packages/api/celery_app.py
/packages/api/app/workers/tasks.py
/packages/api/app/routes/workflows.py


Workflow JSON schema

{
  "name":"WeeklySummary",
  "steps":[
    {"id":"s1","tool":"http_request","input":{"url":".."}},
    {"id":"s2","tool":"parse","input":{"from_step":"s1"}}
  ],
  "retry_policy":{"max_attempts":3,"backoff":"exponential"}
}


Behavior

Orchestrator stores workflow state in DB; workers pick up steps from queue.

Reactive engine can insert new steps or route to alternative branches on exceptions.

Persona

Start with simple FIFO + retries; add DAG/branching after tests pass.

Logs for each step must be human readable.

Acceptance

Create a workflow, execute it via workers, view step logs.

Failure triggers retry and updates workflow status.

Commit plan

feat(m4): add orchestrator state machine

feat(m4): add celery worker tasks

test(m4): orchestrator integration tests

M5 — Local Agent (OS control) + IoT Integration

Goal: Add safe OS-level control via a local signed daemon, plus IoT integrations (Home Assistant, MQTT, Matter).

Deliverables

Local Agent Daemon (runs on user's machine) with mutually authenticated connection to cloud agent.

Signed commands & approval flow.

Capabilities manifest for local agent (open_app, file_move, screenshot, run_script) — run_script limited to whitelist.

IoT integration layer: connectors for MQTT, Home Assistant, and optional Matter bridge.

Files

/packages/local_agent/agent_daemon.py
/packages/local_agent/capabilities.json
/packages/api/app/adapters/local_agent_adapter.py
/packages/api/app/tools/iot_tool.py


Security

Mutual TLS or signed JWT with nonce for each command.

Local UI confirmation modal for sensitive commands (or user-configured non-interactive mode with strict policies).

Default: destructive capabilities require explicit per-command approval.

Persona

Add local agent only after explicit user opt-in on each host.

Never allow cloud agent to run arbitrary scripts on local machine without signed/approved manifest.

Acceptance

Local agent registers with cloud agent and executes a non-destructive command (e.g., open calculator) after validation.

IoT connector can toggle a test device (or simulate if not available).

Commit plan

feat(m5): add local agent daemon scaffold

feat(m5): add adapter and capabilities manifest

test(m5): handshake + sample command test

M6 — UI Dashboard & Human-in-the-loop

Goal: Web UI to start goals, review plans, approve flagged steps, inspect logs, manage tools/agents.

Deliverables

React app with pages: Dashboard, Agent view, Workflow editor, Tool Manager, Memory explorer, Approval modal.

WebSocket for real-time updates.

Role-based access control for approvals (simple RBAC).

Files

/packages/ui/src/pages/Dashboard.tsx
/packages/ui/src/pages/AgentView.tsx
/packages/ui/src/components/ApprovalModal.tsx
/packages/api/app/routes/ws.py
/packages/ui/src/services/api.ts


Persona

Keep UI minimal initially (one dashboard + task detail).

Approval modal must show exact step data & required permissions.

One component per commit.

Acceptance

User starts a goal from UI → sees steps → can approve steps that requires_approval.

Real-time logs stream to Dashboard.

Commit plan

feat(m6): add Dashboard page

feat(m6): add Task Detail view + Approval modal

test(m6): integration test for approval flow

M7 — Safety, Policy Engine, Audit & Monitoring

Goal: Harden the system: safety rules, audit trails, observability and secrets management.

Deliverables

Safety rules engine: allowlists/deny-lists, rate limits, anomaly detection.

Audit logs with immutable entries for every step change.

Prometheus metrics + Grafana dashboards.

Emergency stop / kill-switch API.

Secrets integration: Vault / cloud KMS (or dotenv for dev).

Files

/packages/api/app/security/safety_engine.py
/packages/api/app/logs/audit.py
/infra/monitoring/prometheus.yml
/infra/monitoring/grafana/*
/packages/api/app/routes/admin.py


Persona

Safety engine enforced before enabling new connectors or tools that access system/finance/IoT.

Any connector touching finance requires manual sign-off.

Acceptance

Safety engine blocks a disallowed action and logs the block.

Audit export for a task lifecycle.

Commit plan

feat(m7): add safety engine skeleton

chore(m7): add audit logging

ops(m7): add monitoring scaffold

M8 — Domain Connectors & Personalization

Goal: Add concrete domain connectors and a preference/profile manager for personalization.

Domains (each separate workstream)

Communications: Gmail (OAuth-safe), Slack, Discord.

Productivity: Google Calendar, Notion, Trello.

Finance: Stripe (payments), Plaid (bank access) — strict approval/opt-in.

Health: Fitbit / Apple Health (read-only unless opt-in).

Travel: Skyscanner / Amadeus for itineraries.

Deliverables

Connector adapters with OAuth flows, dry-run support, rate limiting.

Profile & Preference Manager: learns habits and provides personalized suggestions.

Files

/packages/api/app/connectors/gmail_connector.py
/packages/api/app/connectors/calendar_connector.py
/packages/api/app/memory/profile_manager.py


Persona

Each connector is a separate PR/commit. Secrets never in source.

Finance connectors require explicit double opt-in and security review.

Acceptance

Connector can perform a dry-run (e.g., compose email but not send) and record result.

Profile manager updates user preferences from interactions.

Commit plan

feat(m8): add gmail connector (dry-run)

feat(m8): add calendar connector

feat(m8): add profile manager

M9 — Creative & Research Assistant + Production Hardening

Goal: Final capabilities for knowledge work: retrieval-augmented research, generative content, slide/asset generation, and production hardening.

Deliverables

Research tool: document ingestion, RAG pipelines, report generator, export (PDF/slides).

Content tool: creative prompts templates, image prompt scaffolds.

Learning assistant: tailored study plans, spaced repetition integration.

Production ops: containerization, helm charts / terraform, autoscaling for workers, e2e tests, chaos tests.

Files

/packages/api/app/tools/research_tool.py
/packages/api/app/tools/content_tool.py
/infra/k8s/*
/infra/terraform/*
/tests/e2e/*


Persona

Generated outputs are REVIEW-ONLY by default (no auto-sharing or posting).

Any publishing or payment actions require user confirmation.

Acceptance

Generate a short research summary from ingested docs and export a PDF.

Production deploy using infra manifests.

Commit plan

feat(m9): add research tool

feat(m9): add content tool

ops(m9): production infra manifests + e2e tests

Final repo target tree (after M9)
/README.md
/ARCHITECTURE.md
/docker-compose.yml
/.devcontainer/
/packages/
  /api/
    app/
      main.py
      routes/
      agent/
      orchestrator/
      memory/
      tools/
      connectors/
      security/
      workers/
      db/
  /ui/
    src/
  /llm/        # AnythingLLM integration shim & adapter
  /local_agent/
  /tools/      # optional: utility scripts
/migrations/
/infra/
  /k8s/
  /terraform/
  /monitoring/
/tests/
  /unit/
  /integration/
  /e2e/

How this resolves the confusion & session split

Single canonical plan: This message is the unified authoritative milestone plan. Use it as the only source-of-truth across sessions.

Session mapping suggestion (practical):

Keep one ChatGPT session per concurrent milestone or a named mapping (e.g., “Session-M0”, “Session-M1”). But the canonical plan above is the contract each session follows.

When a session finishes a milestone, update the canonical plan with a short “changes” note and commit files to the repo so other sessions can pick up code from the repo rather than conversation state.

Safety/checkpoints (explicit)

Any tool with permissions.system==true or permissions.filesystem==true will be gated by:

Local host opt-in.

Admin approval via UI with task details + reason.

Signed command token for the local agent.

Finance & payment connectors require manual security review before enabling.

Tests & QA approach (applies to all milestones)

Unit tests for each module.

Integration tests:

Planner → Executor (M1)

Registry → Runner (M2)

Memory retrieval + planner (M3)

Worker end-to-end for orchestrator (M4)

E2E tests for major workflows (M6+).

Code coverage checks in CI.

Commit / PR style (persona)

Commit messages: scope(m#): short description (e.g., feat(m2): add tool registry).

Each PR includes:

Purpose and how it advances the vision.

Tests added/updated.

Run steps & smoke tests in README.

Security notes if applicable.