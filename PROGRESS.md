# Project Progress

## What This Project Is

A Trello-style kanban board behind "Sign in with Google" — the combination of two earlier learning
projects:

- **GoogleOAuthProject** → the hand-rolled OAuth 2.0 / OIDC auth layer
- **ToDoListApp** → the FastAPI + Svelte 5 app skeleton, plus its never-done Neon PostgreSQL migration

Design doc: `docs/superpowers/specs/2026-07-08-kanban-app-design.md`
Knowledge base: `KNOWLEDGE.md`

## Current State

### Docs — DONE
Design spec, knowledge base, and this progress file written (2026-07-08).

### Implementation plan — NOT STARTED
Next step: run the writing-plans process against the design spec to produce
`docs/superpowers/plans/…`, then implement.

### Backend — NOT STARTED
### Frontend — NOT STARTED

## Setup Checklist (before implementation)

- [ ] Google Cloud console: add `http://localhost:5173/auth/callback` as an authorized redirect
      URI (the GoogleOAuthProject client can be reused)
- [ ] Neon: create a project/database, grab the connection string
- [ ] `backend/.env` from `.env.example`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`,
      `SESSION_SECRET`, `DATABASE_URL`

## How to Run (once built)

### Backend
```
cd backend
python -m uvicorn main:app --reload --port 8001
```

### Frontend
```
cd frontend
npm run dev
```

Frontend at `http://localhost:5173` (Vite proxies `/api` and `/auth` to the backend)
Backend at `http://localhost:8001` · FastAPI docs at `http://localhost:8001/docs`

## Notes

- Port 8001, not 8000 — same convention as ToDoListApp (8000 had stuck processes on this machine).
- The browser only ever talks to `:5173`; the OAuth redirect URI is
  `http://localhost:5173/auth/callback` and must match the Google console entry exactly.
