# Project Progress

## What This Project Is

A Trello-style kanban board behind "Sign in with Google" — the combination of two earlier learning
projects:

- **GoogleOAuthProject** → the hand-rolled OAuth 2.0 / OIDC auth layer
- **ToDoListApp** → the FastAPI + Svelte 5 app skeleton, plus its never-done Neon PostgreSQL migration

Design doc: `docs/superpowers/specs/2026-07-08-kanban-app-design.md`
Implementation plan: `docs/superpowers/plans/2026-07-08-kanban-app.md`
Knowledge base: `KNOWLEDGE.md`
Working agreement: `CLAUDE.md` (local, untracked) — Claude teaches, the human implements.

## Current State

### Docs — DONE (2026-07-08)

### Scaffolding — DONE (2026-07-08, by Claude per direct instruction)
Full structure exists; every function the human implements is stubbed with its contract,
a `TODO(Task N)` marker matching the plan, and `raise NotImplementedError` where applicable.
All HTML/CSS is complete (off-curriculum by agreement) — the Svelte components have finished
markup and styles with stubbed logic; the frontend builds clean.

**The stub map (what YOU implement, in plan order):**

| File | Task |
|------|------|
| `backend/config.py` | 1 |
| `backend/main.py` | 1, 2 |
| `backend/db.py` | 2, 4, 6, 7 |
| `backend/oauth.py`, `backend/tokens.py` | 3 (port from GoogleOAuthProject) |
| `backend/auth.py` | 4 |
| `backend/ordering.py` + `backend/tests/test_ordering.py` | 5 |
| `backend/tests/conftest.py` | 5 |
| `backend/tests/test_columns.py` | 6 |
| `backend/tests/test_cards.py` | 7 |
| `frontend/src/lib/api.js` | 8 |
| `frontend/src/App.svelte` (script TODOs) | 8, 11 |
| `frontend/src/lib/Board.svelte` (function bodies) | 9, 10 |
| `frontend/src/lib/Column.svelte`, `Card.svelte` (drag handlers) | 10 |

### Implementation — NOT STARTED (Task 1 is next)

## Setup Checklist (before Task 1)

- [ ] Google Cloud console: add `http://localhost:5173/auth/callback` as an authorized redirect
      URI (the GoogleOAuthProject client can be reused). For Task 4.4's backend-only test you'll
      temporarily also want `http://localhost:8001/auth/callback`.
- [ ] Neon: create a dev database AND a test database; grab both connection strings
- [ ] `backend/.env` from `backend/.env.example` — all six values

## How to Run — Docker (the default)

```
docker compose up --build
```

- `--build` re-checks both images every start: dependency changes (`requirements.txt`,
  `package.json`) trigger a rebuild; otherwise Docker's layer cache makes it near-instant.
- Code changes need NO rebuild: both directories are bind-mounted, uvicorn runs `--reload`,
  Vite hot-reloads.
- Backend tests inside the container: `docker compose exec backend python -m pytest tests/ -v`

Frontend at `http://localhost:5173` (Vite proxies `/api` and `/auth` to the backend container)
Backend also published at `http://localhost:8001` · FastAPI docs at `http://localhost:8001/docs`

## How to Run — bare metal (fallback)

```
cd backend && python -m uvicorn main:app --reload --port 8001
cd frontend && npm run dev
```

## Notes

- Port 8001, not 8000 — same convention as ToDoListApp (8000 had stuck processes on this machine).
- The browser only ever talks to `:5173`; the OAuth redirect URI is
  `http://localhost:5173/auth/callback` and must match the Google console entry exactly.
- Inside Docker, the Vite proxy targets `http://backend:8001` (service name), configured via
  `BACKEND_ORIGIN` in `docker-compose.yml` — see `frontend/vite.config.js`.
