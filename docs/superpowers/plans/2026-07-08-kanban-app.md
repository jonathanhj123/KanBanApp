# KanBanApp Implementation Plan

> **For agentic workers:** This plan is NOT for autonomous execution. Per `CLAUDE.md`, the human
> implements every task while Claude teaches: explain the thought process, review the human's code,
> never write the implementation. Steps use checkbox (`- [ ]`) syntax so the human can track progress.

**Goal:** A Trello-style kanban board behind hand-rolled "Sign in with Google," with multi-user data
in Neon PostgreSQL.

**Architecture:** FastAPI backend (`:8001`) owns the OAuth flow (ported from GoogleOAuthProject) and
a user-scoped board API over psycopg2/Neon. Svelte 5 SPA (`:5173`) renders the board and hand-rolled
drag-and-drop; the Vite dev proxy makes the session cookie first-party.

**Tech Stack:** Python, FastAPI, Uvicorn, httpx, PyJWT + cryptography, psycopg2-binary,
pydantic-settings, pytest · Svelte 5 (runes), Vite · Neon PostgreSQL.

**Spec:** `docs/superpowers/specs/2026-07-08-kanban-app-design.md` — read it before starting.

## Global Constraints

- Backend port `8001`, frontend port `5173` — exactly (spec + PROGRESS.md).
- OAuth redirect URI: `http://localhost:5173/auth/callback` for the real flow (browser → Vite → backend). Must match the Google console entry exactly.
- Users keyed on the Google `sub` claim — never email.
- **Every** SQL query is scoped to the logged-in user; cards are reached only via `columns.user_id`.
- Parameterized SQL only (`%s` placeholders) — never string formatting.
- Objects that exist but aren't yours → `404` (don't leak existence).
- Secrets (`GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `SESSION_SECRET`, `DATABASE_URL`) live in `backend/.env`, git-ignored; `backend/.env.example` is the committed template.
- Card/column ids: Python-generated UUID strings (TEXT in the DB).
- Commit at the end of every task, and after any green test run worth keeping.

> **Scaffolding note (2026-07-08):** the full file structure already exists — every function below
> is stubbed with its contract and a `TODO(Task N)` marker, and all HTML/CSS is pre-built (off
> curriculum by agreement, see CLAUDE.md). "Create:" in a task therefore means "fill in the stub."
> The project also runs under Docker now: `docker compose up --build` replaces the bare
> uvicorn/npm commands in the steps below — full run instructions live in PROGRESS.md.

## How to work each task (the learning loop)

1. Read the task's **Why** and **Thought process** with Claude — ask until it makes sense.
2. Write the failing test first where the task has one (TDD is part of the curriculum).
3. Implement until green. You type the code; Claude reviews and explains, per `CLAUDE.md`.
4. Run the **Verify** commands; update `KNOWLEDGE.md`'s Learning Log if you learned something non-obvious.
5. Commit with the suggested message.

---

### Task 1: Backend skeleton + configuration

**Files:**
- Create: `backend/requirements.txt`, `backend/.env.example`, `backend/.env` (local only), `backend/config.py`, `backend/main.py`

**Interfaces:**
- Produces: `config.settings` — a pydantic-settings object with attributes `google_client_id`, `google_client_secret`, `session_secret`, `database_url`, `redirect_uri` (all `str`). Later tasks import `from config import settings`.
- Produces: `main.app` — the FastAPI instance with `SessionMiddleware` installed, `GET /api/health` → `{"status": "ok"}`.

**Why this task:** Every later piece needs configuration and an app to hang routes on. Doing it first
also front-loads the two classic setup failures (missing env vars, port conflicts) while the system
is still tiny enough to debug them instantly.

**Thought process to discuss before coding:**
- Why pydantic-settings instead of `os.environ` reads scattered through the code (single validated
  object, fails loudly at startup, one place to see every knob).
- Why `SessionMiddleware` needs a real secret: the cookie is *signed* — the server can detect
  tampering, but the contents are readable. What does that imply about what we may store in it?
  (Answer to reach: opaque ids like `sub` are fine; secrets are not.)

**Steps:**

- [ ] **1.1** Write `requirements.txt`: fastapi, uvicorn, httpx, pyjwt, cryptography, psycopg2-binary, pydantic-settings, python-multipart is NOT needed — discuss why each line is there before adding it. Create a venv and install.
- [ ] **1.2** Write `.env.example` with the four secrets above plus `REDIRECT_URI=http://localhost:5173/auth/callback`; copy to `.env` and fill in real values (Google creds can be copied from GoogleOAuthProject's `.env` for now).
- [ ] **1.3** Write `config.py` (pydantic-settings `BaseSettings` subclass reading `.env`).
- [ ] **1.4** Write `main.py`: FastAPI app, `SessionMiddleware` with `settings.session_secret`, `GET /api/health` route.
- [ ] **1.5** Verify: `python -m uvicorn main:app --reload --port 8001` from `backend/`, then `curl http://localhost:8001/api/health` → `{"status":"ok"}`. Also verify startup *fails* with a clear error when `.env` is missing a variable (rename it briefly) — that's the pydantic-settings lesson.
- [ ] **1.6** Check `git status` shows `.env` is NOT staged (the root `.gitignore` should already cover it — confirm). Commit: `feat: backend skeleton with validated config and session middleware`

---

### Task 2: Database layer — connection + schema

**Files:**
- Create: `backend/db.py`
- Modify: `backend/main.py` (startup hook)

**Interfaces:**
- Produces: `db.get_connection() -> psycopg2 connection` (reads `settings.database_url`).
- Produces: `db.create_tables() -> None` — idempotent, creates `users`, `columns`, `cards` exactly as in the spec's SQL (TEXT ids, FKs with `ON DELETE CASCADE`, `position INTEGER NOT NULL`).
- Produces: `main.py` calls `create_tables()` on startup (FastAPI `lifespan` — the modern replacement for the deprecated `@app.on_event("startup")` mentioned in the old ToDoListApp notes).

**Why this task:** This is the Neon/psycopg2 lesson imported from ToDoListApp. Isolated here so that
when something goes wrong it can only be connection-or-SQL, not app logic.

**Thought process to discuss:**
- The psycopg2 mental model: connection → cursor → execute → fetch → commit. What's a transaction
  and when does anything actually persist?
- Why `CREATE TABLE IF NOT EXISTS` (idempotency: startup must be safe to run twice).
- Why `ON DELETE CASCADE` on both FKs (delete a user → their columns go → their cards go; the DB
  enforces it so app code can't forget).
- Copy schema **from the spec**, don't retype from memory — schema drift between doc and DB is a
  classic bug class.

**Steps:**

- [ ] **2.1** Create the Neon project/database in their console; put the connection string in `.env` as `DATABASE_URL`.
- [ ] **2.2** Write `get_connection()` and `create_tables()` in `db.py`.
- [ ] **2.3** Wire `create_tables()` into startup via lifespan in `main.py`.
- [ ] **2.4** Verify: start the server, then in Neon's SQL editor run `\dt`-equivalent (`SELECT table_name FROM information_schema.tables WHERE table_schema='public';`) → the three tables exist. Restart the server → no error (idempotency proven).
- [ ] **2.5** Commit: `feat: db connection and idempotent schema creation`

---

### Task 3: Port the OAuth modules

**Files:**
- Create: `backend/oauth.py`, `backend/tokens.py` (ported from `../GoogleOAuthProject/app/`)

**Interfaces:**
- Produces: `oauth.make_state() -> str`, `oauth.make_pkce_pair() -> tuple[str, str]` (verifier, challenge), `oauth.build_auth_url(state: str, code_challenge: str) -> str`, `oauth.exchange_code(code: str, code_verifier: str) -> dict` (the token response).
- Produces: `tokens.verify_id_token(id_token: str) -> dict` (verified claims; raises on any failed check).
- (If the originals use different names, keep the originals' names and update this block — the point is that Task 4 must call exactly what exists.)

**Why this task:** This is the "combine the two projects" moment. It's a *port*, not a rewrite — but
per the learning goal, the port is done by re-reading, not blind copy-paste.

**Thought process to discuss:**
- Re-walk the flow using `../GoogleOAuthProject/KNOWLEDGE.md` §3 and §5: what attack does `state`
  stop, what attack does PKCE stop, what do the four ID-token checks (signature/`iss`/`aud`/`exp`)
  each block? You should be able to answer all four *before* porting.
- What actually changes in the port: config import paths, and `redirect_uri` now comes from
  settings (`:5173`, not `:8000`). Everything protocol-level stays identical.

**Steps:**

- [ ] **3.1** Read both source files in GoogleOAuthProject end-to-end; for each function, say out loud (to Claude) what it does and why it exists. Claude checks understanding, not vibes.
- [ ] **3.2** Port `oauth.py`, adjusting only config wiring. Same for `tokens.py`.
- [ ] **3.3** Google Cloud console: add `http://localhost:5173/auth/callback` as an authorized redirect URI on the existing OAuth client.
- [ ] **3.4** Verify (import-level only for now): `python -c "import oauth, tokens"` from `backend/` with the venv active — no import errors; full-flow verification happens in Task 4/7.
- [ ] **3.5** Commit: `feat: port hand-rolled oauth + id-token verification from GoogleOAuthProject`

---

### Task 4: Auth routes, user upsert, and the auth dependency

**Files:**
- Create: `backend/auth.py`
- Modify: `backend/db.py` (user functions), `backend/main.py` (include router)

**Interfaces:**
- Produces (db.py): `upsert_user(sub: str, email: str, name: str | None, picture: str | None) -> bool` (returns True if the user was newly created), `get_user(user_id: str) -> dict | None`, `seed_default_columns(user_id: str) -> None` (inserts To Do / Doing / Done at positions 0,1,2).
- Produces (auth.py): router with `GET /auth/login`, `GET /auth/callback`, `POST /auth/logout`; and `get_current_user(request: Request) -> dict` — a FastAPI dependency returning the user row or raising `HTTPException(401)`.
- Consumes: everything from Tasks 1–3 (`settings`, `get_connection`, `oauth.*`, `tokens.verify_id_token`).

**Why this task:** This is the spec's headline upgrade — the OAuth demo becomes a multi-user app.
The callback gains exactly one new responsibility: turning verified claims into a DB row.

**Thought process to discuss:**
- `INSERT ... ON CONFLICT (id) DO UPDATE` — what "upsert" means, why we update name/picture/email on
  every login (people change avatars), and why the *key* never changes (`sub`).
- How to know a user is new (so we seed columns exactly once). Postgres trick to reach:
  `ON CONFLICT ... DO UPDATE ... RETURNING (xmax = 0)` is clever but obscure — a simpler
  SELECT-first inside the same transaction is fine and clearer. Discuss the trade-off, pick one.
- Why `get_current_user` is a *dependency* rather than a decorator or middleware: FastAPI injects
  it per-route, routes declare their auth need in their signature, and tests can override it.
- Error paths land on the frontend login page with a message: callback failures redirect to
  `/?error=...` rather than returning JSON (the browser is mid-redirect, not mid-fetch).

**Steps:**

- [ ] **4.1** Write the db functions (`upsert_user`, `get_user`, `seed_default_columns`). Parameterized SQL; one transaction for upsert+seed.
- [ ] **4.2** Write `/auth/login` (state + PKCE into session, redirect to Google) and `/auth/callback` (state check → exchange → verify → upsert → maybe-seed → store `sub` in session → redirect to `/`). Write `/auth/logout` (clear session, redirect to `/`).
- [ ] **4.3** Write `get_current_user` and a temporary protected route `GET /api/me` in `main.py` that returns the current user dict.
- [ ] **4.4** Verify without a frontend: temporarily set `REDIRECT_URI=http://localhost:8001/auth/callback` in `.env` **and** add that URI in the Google console; do the full login in a browser at `http://localhost:8001/auth/login`; then `GET /api/me` in the same browser shows your identity. Check Neon: your `users` row exists and columns are seeded exactly once even after logging in twice. Set `REDIRECT_URI` back to `:5173` when done.
- [ ] **4.5** Verify the failure path: hit `/auth/callback?state=wrong&code=x` → redirected to `/?error=...`, not a 500.
- [ ] **4.6** Commit: `feat: auth routes with user upsert, column seeding, and auth dependency`

---

### Task 5: Test infrastructure + pure reorder logic (TDD)

**Files:**
- Create: `backend/ordering.py`, `backend/tests/test_ordering.py`, `backend/tests/conftest.py`
- Modify: `backend/requirements.txt` (add pytest)

**Interfaces:**
- Produces: `ordering.reorder(ids: list[str], moved_id: str, target_index: int) -> list[str]` — pure function: remove `moved_id` from `ids` if present, insert at `target_index` (clamped to valid range); the returned list's indexes ARE the new `position` values.
- Produces (conftest.py): a `client` pytest fixture — FastAPI `TestClient` with `get_current_user` overridden via `app.dependency_overrides` to return a fixed fake user; a `test_db` fixture pointing at `TEST_DATABASE_URL` (a separate Neon database or branch) that creates tables and truncates all three between tests.

**Why this task:** Two lessons at once. First, TDD on a pure function — the easiest possible place
to learn the red/green rhythm. Second, the dependency-override trick that lets every later API test
run without Google.

**Thought process to discuss:**
- Why extract `reorder` as a pure function at all (testable without a DB; the DB layer just
  `UPDATE`s positions from `enumerate(result)`).
- Test design: what are the *interesting* inputs? Reach this list together — move within a column
  (forward and backward — off-by-one territory), move into another column's list, target_index
  past the end (clamp), moving to where it already is (no-op), moved_id not in the list (cross-column case).
- Why tests get a separate database (your dev board would be truncated otherwise) and why
  `dependency_overrides` beats mocking the session cookie.

**Steps:**

- [ ] **5.1** Write `tests/test_ordering.py` — one test per interesting input from the discussion, written BEFORE `ordering.py` exists.
- [ ] **5.2** Run: `python -m pytest tests/ -v` from `backend/` → all FAIL (module not found / assertions). Confirm they fail for the *right reason*.
- [ ] **5.3** Implement `ordering.reorder`. Run again → all PASS.
- [ ] **5.4** Write `tests/conftest.py` (fixtures described above). Create the test database in Neon; add `TEST_DATABASE_URL` to `.env` and `.env.example`.
- [ ] **5.5** Smoke-test the fixtures: a trivial test that calls `GET /api/me` through the overridden client and asserts the fake user comes back.
- [ ] **5.6** Commit: `feat: reorder logic (TDD) and test fixtures with auth override`

---

### Task 6: Board API — columns + board read

**Files:**
- Create: `backend/api.py`, `backend/tests/test_columns.py`
- Modify: `backend/db.py`, `backend/main.py` (include router, move `/api/me` into `api.py`)

**Interfaces:**
- Produces (db.py): `get_board(user_id) -> list[dict]` (columns ordered by position, each with nested `cards` ordered by position), `create_column(user_id, title) -> dict`, `rename_column(user_id, column_id, title) -> dict | None`, `delete_column(user_id, column_id) -> bool` (None/False = not found or not yours).
- Produces (api.py): `GET /api/me`, `GET /api/board` → `{"columns": [...]}`, `POST /api/columns` (body `{"title": str}`, 201), `PATCH /api/columns/{id}` (body `{"title": str}`), `DELETE /api/columns/{id}` (204). All depend on `get_current_user`; missing/not-yours → 404.
- Consumes: fixtures from Task 5.

**Why this task:** First real user-scoped CRUD. The pattern established here (db function returns
None for not-yours → route turns that into 404) repeats for cards, so getting it right once matters.

**Thought process to discuss:**
- `get_board` query strategy: two queries (all my columns; all cards JOINed through my columns)
  assembled in Python, per the spec's lean. Walk through *why* one JOIN-everything query makes the
  nesting awkward (row explosion, group-by-in-Python anyway).
- Where new columns get their `position` (max+1 within the user's columns — inside the INSERT via a
  subquery, or SELECT-then-INSERT in a transaction; discuss race conditions at learning depth, pick simple).
- Request/response validation with Pydantic models: what FastAPI does for free (422s) vs what we
  still check ourselves (ownership).

**Test cases for `tests/test_columns.py` (write first, watch fail, implement, watch pass):**
- Board starts empty for a fresh user; after two `POST /api/columns`, `GET /api/board` returns both in creation order with correct positions.
- Rename works and persists; renaming a nonexistent column id → 404.
- **The ownership test** (most important in the file): insert a column for a *different* user id directly via db functions; PATCH and DELETE on it as the fake user → 404, and the row is unchanged.
- DELETE removes the column; board reflects it.
- Unauthenticated request (a client *without* the override) → 401.

**Steps:**

- [ ] **6.1** Write the five test cases above; run → FAIL.
- [ ] **6.2** Implement db functions, then routes, until green. Claude reviews the SQL for scoping and parameterization line by line.
- [ ] **6.3** Run the full suite: `python -m pytest tests/ -v` → everything green (Task 5 tests still pass).
- [ ] **6.4** Commit: `feat: user-scoped column CRUD and board read`

---

### Task 7: Board API — cards + move

**Files:**
- Create: `backend/tests/test_cards.py`
- Modify: `backend/db.py`, `backend/api.py`

**Interfaces:**
- Produces (db.py): `create_card(user_id, column_id, text) -> dict | None` (None if column isn't yours; position = end of column), `update_card_text(user_id, card_id, text) -> dict | None`, `move_card(user_id, card_id, new_column_id, new_position) -> bool` (uses `ordering.reorder`, renumbers affected column(s) in ONE transaction), `delete_card(user_id, card_id) -> bool`.
- Produces (api.py): `POST /api/cards` (body `{"column_id", "text"}`, 201), `PATCH /api/cards/{id}` (body either `{"text"}` or `{"column_id", "position"}`), `DELETE /api/cards/{id}` (204).
- Consumes: `ordering.reorder` from Task 5, patterns from Task 6.

**Why this task:** The heart of kanban — and the first multi-statement transaction (move = update
card + renumber up to two columns; partial application must be impossible).

**Thought process to discuss:**
- Ownership through the JOIN: cards have no `user_id`, so every card query joins `columns` and
  filters `columns.user_id = %s`. Write one together on paper before coding.
- The move algorithm, step by step: load target column's ordered card ids → `reorder(...)` →
  `UPDATE` each id's position (+ the moved card's `column_id`) → if it changed columns, renumber the
  source column too → commit. What happens if step 3 fails halfway and why the transaction saves us.
- The PATCH route's two shapes (`text` vs `column_id`+`position`): how to model that with Pydantic
  (optional fields + a validation check) and why one endpoint (the frontend thinks "update this card").

**Test cases for `tests/test_cards.py`:**
- Create three cards in a column → positions 0,1,2; text edit persists.
- Move within a column (position 2 → 0) → new order verified via `GET /api/board`, positions still 0..n-1 contiguous.
- Move across columns → source column's positions re-contiguous, target ordered correctly, card's `column_id` changed.
- Move to another user's column → 404, nothing changed anywhere.
- Card ops on another user's card → 404 (the JOIN-scoping test).
- Delete → gone from board; deleting a column deletes its cards (CASCADE proof through the API).

**Steps:**

- [ ] **7.1** Write the test cases; run → FAIL.
- [ ] **7.2** Implement db functions (move first — it's the hard one), then routes, until green.
- [ ] **7.3** Full suite green. Update `KNOWLEDGE.md` Learning Log with anything the transaction work taught you.
- [ ] **7.4** Commit: `feat: card CRUD and transactional move with renumbering`

---

### Task 8: Frontend scaffold — Vite proxy, session check, login page

**Files:**
- Create: `frontend/` (Vite + Svelte scaffold), `frontend/vite.config.js` (proxy), `frontend/src/lib/api.js`, `frontend/src/lib/Login.svelte`
- Modify: `frontend/src/App.svelte`

**Interfaces:**
- Produces (api.js): `apiFetch(path, options?) -> parsed JSON` — thin wrapper over `fetch` that sets JSON headers, throws a typed error object `{status, message}` on non-2xx so callers can branch on `err.status === 401`.
- Produces (App.svelte): on mount, calls `/api/me`; state machine `loading → loggedIn(user) → board` | `loggedOut → Login`. Reads `?error=...` from the URL and passes it to Login.
- Produces (vite.config.js): `/api` and `/auth` proxied to `http://localhost:8001`.

**Why this task:** The proxy is the load-bearing piece of the whole SPA+cookie design — prove it
works with the smallest possible frontend before building the board on top.

**Thought process to discuss:**
- Trace one login through the proxy on paper: browser hits `:5173/auth/login` → Vite forwards →
  FastAPI redirects to Google → Google redirects to `:5173/auth/callback` → Vite forwards → FastAPI
  sets the cookie → browser stores it against `:5173`. Where would this break *without* the proxy?
- Why the login button is a plain `<a href="/auth/login">` and not a `fetch` (the browser must
  *navigate* — redirects and cookies are navigation-level, and fetch would try to follow the
  redirect to Google cross-origin and die).
- Svelte 5 recap from ToDoListApp: `$state`, `$derived`, `onMount`-equivalent with `$effect`.

**Steps:**

- [ ] **8.1** Scaffold: `npm create vite@latest frontend -- --template svelte` (plain JS), install, strip demo content.
- [ ] **8.2** Add the proxy config; write `api.js`; write `App.svelte`'s session check and `Login.svelte` (button + error slot).
- [ ] **8.3** Verify end-to-end: both servers running, browser at `http://localhost:5173`, full Google login lands you back with your name/picture rendered from `/api/me`. Cancel on the consent screen → login page shows the error message. Logout works.
- [ ] **8.4** Confirm in devtools: the session cookie lives on `localhost:5173`, and no request ever goes to `:8001` directly.
- [ ] **8.5** Commit: `feat: frontend scaffold with vite proxy, session check, login page`

---

### Task 9: Board rendering + column/card CRUD (no drag yet)

**Files:**
- Create: `frontend/src/lib/Board.svelte`, `frontend/src/lib/Column.svelte`, `frontend/src/lib/Card.svelte`
- Modify: `frontend/src/App.svelte`

**Interfaces:**
- Produces (Board.svelte): owns `board` state (`$state` of the `GET /api/board` shape); passes each column + callback props down; add-column input at the end of the row.
- Produces (Column.svelte): props `column`, callbacks for rename/delete/addCard/…; click-to-edit title; add-card input; renders `Card` list.
- Produces (Card.svelte): props `card` + callbacks; inline edit on click, delete button.
- Consumes: `apiFetch`, all Task 6/7 endpoints.

**Why this task:** Gets the full CRUD loop working with plain clicks before drag-and-drop adds event
complexity on top. If something breaks in Task 10, you'll know it's the drag code.

**Thought process to discuss:**
- State ownership: one `board` object in Board.svelte, children mutate via callbacks — why this beats
  each Column fetching its own data (single source of truth, one refetch path). Compare with how
  ToDoListApp's App.svelte owned the todos array.
- After a mutation: refetch the whole board vs surgically patch local state? Start with refetch
  (simple, always consistent); optimistic updates arrive with drag in Task 10. This "correct first,
  fast second" ordering is itself the lesson.
- Component boundaries: what each of the three components would need to know to be reused — keep
  Card dumb (props in, events out).

**Steps:**

- [ ] **9.1** Build Board.svelte: fetch board, render columns, add-column input.
- [ ] **9.2** Build Column.svelte and Card.svelte with all CRUD interactions, refetch-after-mutate.
- [ ] **9.3** Verify in the browser: create/rename/delete columns; add/edit/delete cards; refresh the page → everything persisted; check the Network tab and explain each request to Claude.
- [ ] **9.4** Verify multi-user isolation for real: log in with a second Google account (or an incognito window) → empty seeded board, no bleed-through.
- [ ] **9.5** Commit: `feat: board ui with full column/card crud`

---

### Task 10: Drag-and-drop with optimistic updates

**Files:**
- Modify: `frontend/src/lib/Board.svelte`, `frontend/src/lib/Column.svelte`, `frontend/src/lib/Card.svelte`

**Interfaces:**
- Consumes: `PATCH /api/cards/{id}` with `{column_id, position}` from Task 7.
- Produces: cards draggable within and across columns; optimistic local move; revert + error message on server failure.

**Why this task:** The headline frontend lesson, isolated at the end so everything under it is known-good.

**Thought process to discuss:**
- The HTML5 DnD contract: `draggable="true"` + `dragstart` (stash card id in `dataTransfer`);
  drop targets must `preventDefault()` on `dragover` or `drop` never fires — THE classic gotcha,
  worth experiencing once before fixing.
- Computing the target position from the drop: simplest correct version first (drop on a column =
  append to end), then refine to drop-between-cards using the hovered card's index. Two iterations,
  both committed.
- Optimistic updates as a pattern: snapshot state → mutate locally → PATCH → on failure restore
  snapshot + show message. Why snapshot/restore beats trying to compute the inverse move.
- Testing failure honestly: stop the backend (or temporarily make the endpoint return 500) and
  watch the revert happen.

**Steps:**

- [ ] **10.1** Implement drag within a column, drop-on-column-appends version, optimistic with revert.
- [ ] **10.2** Verify: drag around, refresh → order persisted. Kill the backend mid-drag → card snaps back + message. Commit: `feat: drag-and-drop cards with optimistic updates`
- [ ] **10.3** Refine to drop-between-cards (insert at hovered index), cross-column included.
- [ ] **10.4** Verify the full matrix: within-column up/down, cross-column to top/middle/end, and persistence after refresh. Second browser window sees the change after ITS next refetch (no realtime — that's fine, note it in KNOWLEDGE.md).
- [ ] **10.5** Commit: `feat: positional drop targets for drag-and-drop`

---

### Task 11: Wrap-up — error polish, docs, retrospective

**Files:**
- Modify: `frontend/src/App.svelte` / `api.js` (401 handling), `PROGRESS.md`, `KNOWLEDGE.md`, `README.md`

**Why this task:** The difference between "it works" and "it's finished": expired sessions don't
strand the user, and the docs tell the truth about the final state.

**Steps:**

- [ ] **11.1** Global 401 handling: any `apiFetch` 401 flips App state to loggedOut with a "session expired" message. Verify by deleting the session cookie in devtools mid-session and clicking anything.
- [ ] **11.2** Sweep the OAuth failure paths once more from the frontend: cancelled consent, bad state (hand-craft the URL), each shows a readable message on the login page.
- [ ] **11.3** Run the whole backend suite one final time: `python -m pytest tests/ -v` → green.
- [ ] **11.4** Update `PROGRESS.md` (state: built; how-to-run confirmed against reality), `README.md` (what this is, setup incl. Google console + Neon steps), and a `KNOWLEDGE.md` Learning Log retrospective: the three hardest bugs and what each taught.
- [ ] **11.5** Commit: `docs: final progress, readme, and retrospective` — then decide together what's next (stretch goals live in the spec).

---

## Post-plan notes

- **Task order is dependency order** — don't skip ahead; each task assumes the previous ones' interfaces exist.
- **Stretch goals** (multiple boards, card details, fractional indexing, refresh tokens) are in the spec, deliberately not planned here. Plan the next one only when this plan is done.
- If an interface named here turns out wrong during implementation, update this plan file in the same commit that changes the code — the plan must stay truthful.
