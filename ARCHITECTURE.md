# Architecture (Initial Draft)

This repo is structured as a monorepo:

- `packages/api/` → FastAPI backend for the agent core
- `packages/ui/` → React frontend (Vite or Next.js)
- `docker-compose.yml` → Dev services (Postgres, Redis, MinIO, API, UI)

Next milestones will add planner, tools, memory, orchestration, and local agent.
