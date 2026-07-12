# Project Progress

## What This Project Is

A Trello-style kanban board behind "Sign in with Google" — the combination of two earlier learning
projects:

- **GoogleOAuthProject** → the hand-rolled OAuth 2.0 / OIDC auth layer. *Docs only* — that
  project never got past its knowledge base and design doc, so KanBanApp's Task 3 is the first
  actual implementation of the flow, built from `../GoogleOAuthProject/KNOWLEDGE.md`.
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

### Implementation — Tasks 1–2 DONE; Task 3 (OAuth build) IN PROGRESS

Task 3 status (2026-07-12): step 3.1 (the theory gate) **passed** — state/CSRF, PKCE, and the
four ID-token checks discussed and quizzed until solid; lessons in `KNOWLEDGE.md` Learning Log.
Note the plan correction: GoogleOAuthProject turned out to be docs-only (no code ever existed),
so Task 3 is a **first build from `../GoogleOAuthProject/KNOWLEDGE.md`**, not a port — the plan
file's Task 3 section was rewritten accordingly.

**Where we left off / next actions:**
1. Write `make_state()` in `backend/oauth.py` — one-liner via the `secrets` module
   (homework question pending: why `secrets` and not `random`?).
2. Then `make_pkce_pair()` (secrets + sha256 + base64url), `build_auth_url()`, `exchange_code()`,
   then `tokens.py::verify_id_token` (PyJWT + PyJWKClient).
3. Step 3.3 still pending: add `http://localhost:5173/auth/callback` in the Google console.
4. Update the stale "port" header docstrings in `oauth.py` / `tokens.py` while in there.

Task 1 (backend skeleton + config, 2026-07-08): `config.py` (pydantic-settings, six validated
fields) and `main.py` (FastAPI app, SessionMiddleware, `GET /api/health` → 200) implemented by the
human and verified live in Docker. Lessons captured in `KNOWLEDGE.md` Learning Log (env-var
precedence, compose env snapshots, `.gitignore` vs already-tracked files).

Task 2 (db connection + schema, 2026-07-12): `db.get_connection()` / `db.create_tables()` and the
lifespan hook in `main.py` implemented by the human; verified against Neon (three tables present,
clean restart proves idempotency). Lessons in `KNOWLEDGE.md` Learning Log (cursor vs connection
API, commit ownership, lifespan mechanics).

## Setup Checklist (before Task 1)

- [ ] Google Cloud console: add `http://localhost:5173/auth/callback` as an authorized redirect
      URI (the GoogleOAuthProject client can be reused). For Task 4.4's backend-only test you'll
      temporarily also want `http://localhost:8001/auth/callback`.
- [ ] Neon: create a test database (dev database `kanban` exists; `TEST_DATABASE_URL` is still a
      placeholder — needed by Task 5)
- [x] `backend/.env` from `backend/.env.example` — `DATABASE_URL` (→ `kanban` DB, verified),
      `SESSION_SECRET` (real), `REDIRECT_URI` set; Google creds still placeholders (needed Task 3)

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
