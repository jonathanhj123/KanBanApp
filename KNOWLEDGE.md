# KanBanApp Knowledge Base

A living document, same format as GoogleOAuthProject's. It starts seeded with the lessons this
project inherits from its two parents, and grows as we build. New insights go in the **Learning
Log** at the bottom (and get folded into the relevant section if they correct or extend it).

---

## 1. What this project inherits

| From | What we take | Where the detail lives |
|------|--------------|------------------------|
| **GoogleOAuthProject** | The full hand-rolled OIDC flow: `state`, PKCE, back-channel exchange, JWKS verification | `../GoogleOAuthProject/KNOWLEDGE.md` — the definitive reference |
| **ToDoListApp** | FastAPI + Svelte 5 two-process shape, Vite dev server, runes-based components | `../ToDoListApp/PROGRESS.md` |
| **ToDoListApp (unfinished)** | The Neon PostgreSQL migration lesson: psycopg2, cursors, SQL, `.env` secrets | `../ToDoListApp/docs/superpowers/specs/2026-05-24-neon-database-migration-design.md` |

The OAuth knowledge base is **not** duplicated here. This file covers only what's *new* in the
combination.

## 2. OAuth demo → real multi-user app

The demo stored verified claims in a session cookie and stopped there. The upgrade:

- At the callback, after verifying the ID token, **upsert a `users` row keyed on `sub`**
  (`INSERT … ON CONFLICT (id) DO UPDATE`). `sub` is Google's stable user ID; email can change,
  so it's display data, never the key.
- The session now stores just the `sub`; every request resolves it to a DB user.
- A `get_current_user` FastAPI **dependency** is the auth gate: read `sub` from session → load
  user → `HTTPException(401)` if missing. Every `/api` route declares it as a parameter.
- **User-scoped queries** are the discipline that makes it multi-user: every SQL statement filters
  by the current user's id. Cards have no `user_id` of their own — ownership flows through the
  column, so card queries JOIN through `columns.user_id`.
- Objects that exist but belong to someone else return **404, not 403** — don't leak existence.

## 3. SPA + session cookie: why the Vite proxy matters

The OAuth demo was server-rendered, so cookies were trivially first-party. A SPA on `:5173`
talking to an API on `:8001` is **cross-origin**: cookies get fiddly (SameSite, CORS with
credentials). The clean dev answer:

- Vite's dev server proxies `/api` and `/auth` to `http://localhost:8001`.
- The browser only ever sees the `:5173` origin, so the session cookie is first-party and gets
  sent automatically — no CORS config, no `credentials: 'include'` edge cases.
- Consequence: the OAuth **redirect URI is `http://localhost:5173/auth/callback`** (the browser
  hits Vite, Vite forwards to FastAPI). That exact URI must be registered in the Google Cloud
  console — `redirect_uri_mismatch` is still the #1 error.

## 4. Ordering is a data problem

Kanban = ordered lists. The naive-but-instructive approach we start with:

- Each column and card has an integer `position`.
- Moving a card = set its new `column_id` and `position`, then **renumber siblings** in the
  affected column(s) so positions stay 0..n-1.
- This is O(n) writes per move and has concurrency hazards — which is exactly the point; feeling
  that pain is what motivates fractional indexing (the stretch goal), the trick real apps
  (Trello, Figma, Linear) use.

## 5. Drag-and-drop, hand-rolled

HTML5 DnD API, no library:

- Card: `draggable="true"`, `dragstart` puts the card id in `event.dataTransfer`.
- Column: `dragover` must call `preventDefault()` (otherwise `drop` never fires — the classic
  gotcha), `drop` reads the id and computes the target position.
- Pattern: **optimistic update** — mutate local Svelte state immediately, PATCH the server,
  revert + show an error if it fails.

## 6. Postgres/psycopg2 basics (the imported Neon lesson)

- `psycopg2.connect(DATABASE_URL)` → connection; `with conn.cursor() as cur:` → execute/fetch.
- Always **parameterized queries** (`cur.execute("… WHERE id = %s", (id,))`) — never f-strings
  (SQL injection).
- `conn.commit()` or nothing persists; multi-statement moves (renumber + update) belong in one
  transaction.
- Tables created idempotently at startup with `CREATE TABLE IF NOT EXISTS`.
- Neon is just hosted Postgres; the connection string lives in `backend/.env`, git-ignored.

## 7. The Docker dev setup

Both halves run in containers via `docker compose up --build`. The mental model:

- **Images hold dependencies, bind mounts hold code.** The Dockerfiles copy
  `requirements.txt` / `package.json` first and install — that's a cached layer, so `--build` on
  every start is near-free unless dependencies actually changed. Source directories are
  bind-mounted over the image's copy, so saves hit uvicorn `--reload` and Vite HMR directly:
  code changes never need a rebuild.
- **Networking changes inside, not outside.** The browser still sees `localhost:5173` and the
  cookie story is untouched. But *between containers* "localhost" means "this container," so the
  Vite proxy targets the backend by its compose service name (`http://backend:8001`), passed in
  as `BACKEND_ORIGIN`.
- **Two Windows-specific gotchas** handled in the config: bind mounts don't emit file-change
  events (Vite falls back to polling when `BACKEND_ORIGIN` is set), and the image's Linux
  `node_modules` must not be shadowed by the Windows one (an anonymous volume at
  `/app/node_modules` protects it).
- **Secrets stay out of images.** `.dockerignore` excludes `.env`; compose injects it at runtime
  via `env_file`.

---

## Learning Log

New entries go here as we build, dated, newest first.

- **2026-07-08** — Task 1 done. Lessons collected along the way:
  - **pydantic-settings validation errors name the *field*** (`session_secret`), not the env var
    (`SESSION_SECRET`) — it validates the model, and the env var is just one possible source.
  - **Real environment variables beat the `.env` file** in pydantic-settings precedence. In Docker
    this matters doubly: compose's `env_file:` injects values into the container environment
    *at container creation*, so editing `.env` changes nothing until `docker compose up -d`
    recreates the container (`restart` reuses the old snapshot).
  - **`DATABASE_URL` as one string vs discrete `PG*` parts**: providers hand out URLs, Python
    libraries consume URLs (twelve-factor convention); parts are how some deployments *store*
    config, but the URL is how the app *expresses* the connection. Watch percent-encoding if the
    password contains `@ / :`.
  - **`.gitignore` only filters untracked files.** Files committed before the rule existed must be
    evicted with `git rm -r --cached` (leaves them on disk). And `git check-ignore` needs
    `--no-index` to test a rule against an already-tracked file.
  - **Frontend never talks to Postgres** — the Node `pg` driver has no business in
    `frontend/package.json`; all DB access goes through the Python backend.
- **2026-07-08** — Project started. Design at `docs/superpowers/specs/2026-07-08-kanban-app-design.md`.
