# KanBanApp — Design

## Overview

A Trello-style kanban board behind "Sign in with Google" — the deliberate combination of two earlier
learning projects. The hand-rolled OAuth 2.0 / OIDC flow from **GoogleOAuthProject** becomes the auth
layer; the FastAPI + Svelte 5 patterns from **ToDoListApp** become the app skeleton; and the Neon
PostgreSQL migration that ToDoListApp planned but never did lands here as the data layer. The result
is the "next level up" lesson: real users in a database keyed by Google identity, auth-protected APIs,
user-scoped queries, and a drag-and-drop SPA frontend.

## Goals

- Turn the OAuth demo into a real multi-user app: upsert a `users` row keyed on the Google `sub` claim at login
- Learn auth-protected API design: a FastAPI dependency that resolves the session cookie to a user, 401 otherwise
- Learn relational modeling with real foreign keys: users → columns → cards, every query scoped to the logged-in user
- Learn PostgreSQL via psycopg2 against Neon (SELECT/INSERT/UPDATE/DELETE, cursors, .env secrets)
- Learn ordering as a data problem: integer `position` columns with renumbering on move
- Hand-roll drag-and-drop with HTML5 drag events in Svelte 5 — no DnD library
- Learn the SPA + session-cookie pattern: Vite dev proxy makes the backend's cookie first-party

## Non-Goals

- No multiple boards — one board per user, which is just "your columns" (stretch goal)
- No card details: no descriptions, labels, due dates, checklists (stretch goals)
- No sharing or collaboration between users
- No column drag-reordering — `columns.position` is assigned at creation and columns keep that
  order; drag-and-drop applies to cards only (column reordering is a natural follow-on)
- No production deployment — localhost only
- No refresh tokens — login-session identity only, same as the OAuth demo

## User Experience

1. **Login page** — visiting `http://localhost:5173` while signed out shows a single
   "Sign in with Google" button. OAuth failures (cancelled consent, bad `state`) land back here
   with a readable error message.
2. **The board** — after login: the user's name and Google profile picture in a header, and their
   columns left-to-right with cards stacked inside. First-ever login seeds three default columns:
   **To Do / Doing / Done**.
3. **Interactions** — add/rename/delete columns; add/edit/delete cards; drag a card to reorder it
   within a column or drop it into another column. Drops apply optimistically and revert with a
   message if the server rejects them.
4. **Sign out** — clears the session, back to the login page.

## Technical Approach

Two processes, same shape as ToDoListApp:

- **Backend** — FastAPI + Uvicorn on `:8001`. The auth layer is `oauth.py` and `tokens.py` ported
  from GoogleOAuthProject **unchanged in spirit**: state (CSRF), PKCE (S256), back-channel token
  exchange via httpx, ID-token verification against Google's JWKS with explicit `iss`/`aud`/`exp`
  checks. Identity lives in Starlette's signed session cookie.
- **Frontend** — Svelte 5 (runes) + Vite on `:5173`. The Vite dev server proxies `/api` and `/auth`
  to the backend, so the browser never leaves the `:5173` origin and the session cookie is
  first-party. This is the piece that makes SPA + cookie auth "just work."
- **Database** — Neon PostgreSQL via `psycopg2-binary`; `DATABASE_URL` in `backend/.env`
  (git-ignored, with a `.env.example` template alongside `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`,
  `SESSION_SECRET`).

**Redirect URI decision:** because the browser stays on `:5173`, the OAuth redirect URI is
`http://localhost:5173/auth/callback` — Vite proxies the callback request to the backend. Add that
URI to the Google Cloud OAuth client (the existing client from GoogleOAuthProject can be reused by
adding it as a second authorized redirect URI), and set it as `redirect_uri` in backend config.
Remember: the URI must match **exactly** or Google returns `redirect_uri_mismatch`.

### Data model

```sql
CREATE TABLE IF NOT EXISTS users (
    id      TEXT PRIMARY KEY,   -- Google's stable `sub` claim, never email
    email   TEXT NOT NULL,
    name    TEXT,
    picture TEXT
);

CREATE TABLE IF NOT EXISTS columns (
    id       TEXT PRIMARY KEY,
    user_id  TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title    TEXT NOT NULL,
    position INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS cards (
    id        TEXT PRIMARY KEY,
    column_id TEXT NOT NULL REFERENCES columns(id) ON DELETE CASCADE,
    text      TEXT NOT NULL,
    position  INTEGER NOT NULL
);
```

Single board per user ⇒ no `boards` table; the user's board is implied by `columns.user_id`.
Ordering uses integer `position` values renumbered on every move — simple, and it teaches *why*
ordering is a real problem before the fractional-indexing stretch goal.

### Auth flow

Identical to GoogleOAuthProject with one addition at the callback:

1. `GET /auth/login` — generate `state` + PKCE verifier, stash in session, redirect to Google.
2. `GET /auth/callback` — verify `state`, exchange the code (back channel, with `code_verifier`),
   verify the ID token (signature via JWKS, `iss`, `aud`, `exp`).
3. **New:** upsert a `users` row keyed on the token's `sub` (INSERT … ON CONFLICT DO UPDATE for
   name/picture/email). If the user is brand new, seed the three default columns in the same step.
4. Store `sub` in the session; redirect to `/`.
5. `POST /auth/logout` — clear the session.

A `get_current_user` FastAPI dependency reads `sub` from the session, loads the user row, and
raises 401 if either is missing. Every `/api` route depends on it, and **every SQL query filters by
the current user's id** — cards are reached only through columns the user owns.

### API

- `GET /api/me` — `{id, name, email, picture}`
- `GET /api/board` — all columns with nested cards, ordered by `position`, in one response the
  frontend renders directly
- `POST /api/columns` — create (title) · `PATCH /api/columns/{id}` — rename ·
  `DELETE /api/columns/{id}` — delete with its cards
- `POST /api/cards` — create (column_id, text) · `PATCH /api/cards/{id}` — edit text, **or move**
  (new `column_id` + `position`; server renumbers siblings) · `DELETE /api/cards/{id}`

### Frontend structure

```
frontend/src/
├── App.svelte            # session check via /api/me → Login or Board
├── lib/
│   ├── api.js            # fetch wrapper: JSON, credentials, 401 → login state
│   ├── Login.svelte      # the Google button (+ error slot)
│   ├── Board.svelte      # loads /api/board, owns board state, add-column UI
│   ├── Column.svelte     # title editing, card list, drop target
│   └── Card.svelte       # draggable, inline edit/delete
```

Drag-and-drop is hand-rolled: `draggable="true"`, `dragstart`/`dragover`/`drop` handlers, card id
in `dataTransfer`. On drop: update local state optimistically, `PATCH /api/cards/{id}`, revert and
show an error on failure.

## Key Components (backend)

```
backend/
├── .env.example      # GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, SESSION_SECRET, DATABASE_URL
├── requirements.txt  # fastapi, uvicorn, httpx, pyjwt, cryptography, psycopg2-binary, pydantic-settings
├── main.py           # app wiring, session middleware, startup: create tables
├── config.py         # pydantic-settings
├── oauth.py          # ★ ported: build_auth_url(), exchange_code(), PKCE helpers
├── tokens.py         # ★ ported: JWKS fetch, ID-token verification
├── auth.py           # /auth routes + get_current_user dependency + user upsert
├── db.py             # get_connection(), create_tables(), all SQL functions
└── api.py            # /api routes (board, columns, cards)
```

## Error Handling

- OAuth failures → redirect to login page with a human-readable message (each failure mode —
  cancelled consent, `state` mismatch, failed exchange, bad token — teaches a different lesson).
- API: 401 (no session) → frontend swaps to login view; 404 for objects that don't exist **or
  aren't yours** (don't leak existence); 500s return a readable error, and the frontend reverts
  optimistic updates.

## Testing

- **Unit tests** (pytest) for pure logic: position renumbering on card move.
- **API tests** using FastAPI's dependency override to fake `get_current_user` — tests never touch
  Google. Run against a scratch database (a Neon branch is itself a nice lesson).
- **OAuth flow** verified manually end-to-end, as in GoogleOAuthProject.

## Open Questions

- ID generation: UUIDs from Python vs. `SERIAL`/`IDENTITY` in Postgres. Lean: Python UUIDs (matches
  ToDoListApp's TEXT ids and keeps SQL simpler). Decide during implementation.
- Whether `GET /api/board` uses one JOIN query or two queries assembled in Python. Lean: two
  queries — clearer for learning. Decide during implementation.

## Stretch Goals

In rough order of value:

1. **Multiple boards** — a `boards` table, a board-list page, one more relation.
2. **Card details** — description, labels, due dates.
3. **Fractional-index ordering** — replace renumbering with sparse/fractional positions.
4. **Refresh tokens** — `access_type=offline`, silent session renewal.

---
*Designed via /brainstorm on 2026-07-08, combining GoogleOAuthProject and ToDoListApp.*
