# MTrack — Agent Guide

## Structure
- `backend/` — FastAPI + async SQLAlchemy 2.0 + asyncpg + Poetry
- `frontend/` — Vue 3 + Vite + Tailwind CSS + Vue Router
- **Not a monorepo** — each is a standalone project with its own deps
- **No tests** exist anywhere in the repo
- **No CI/CD** in-repo — deployed via external ArgoCD

## Backend
- Entry: `src/main.py` (FastAPI app, also contains `Container` wiring and router includes)
- DI via `dependency-injector` — Container in `src/di.py`
- Config via `.env` + empty `config.yaml` (Pydantic Settings loads both)
- `poetry.toml` sets `create = false` — expects global/active venv
- Dev: `cd backend && poetry install && poetry run uvicorn src.main:app --reload --port 8080`
- Docker: `cd backend && docker buildx build --platform linux/amd64 -t registry/mtrack_be:x.y.z .`
- **No lint/format/typecheck configured** for Python

## Frontend
- Entry: `src/main.js`
- `@` alias → `./src` (configured in `vite.config.js`)
- API client in `src/services/api.js` — talks to backend at `VITE_API_BASE_URL`
- Dev: `cd frontend && npm install && npm run dev`
- Lint: `npm run lint` (runs oxlint + eslint sequentially via `npm-run-all2`)
- Format: `npm run format` (prettier, `--experimental-cli` flag)
- Build: `npm run build`
- Docker: needs `VITE_API_BASE_URL` as `--build-arg`
- Brand tokens via Tailwind: `bg-brand-*`, `text-brand-*`
- Currency symbol: Đ (Vietnamese Dong)
- Node engine: `^20.19.0 || >=22.12.0`

## Key architecture notes
- Backend layers: `repositories/` (raw SQL/query) → `services/` (business logic) → `routers/` (endpoints)
- Routers use `@inject` decorator + `Depends(Provide[Container.xxx_service])` for DI
- Frontend category colors are deterministic from name hash (`stringToColor` in `DashboardView.vue`)
- No generated code, no migrations, no codegen — schema is managed externally via the n8n ingestion pipeline
- Single source of version inside app.version file in the root of the project
