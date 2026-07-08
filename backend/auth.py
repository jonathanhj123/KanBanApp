"""Auth routes + the auth gate — YOUR CODE, Task 4.

router = APIRouter()

  GET  /auth/login     Task 4.2
      make_state() + make_pkce_pair() -> stash state & verifier in
      request.session -> RedirectResponse to build_auth_url(...)

  GET  /auth/callback  Task 4.2 — the demo-becomes-multi-user moment:
      1. state from query must equal state in session (else -> /?error=...)
      2. exchange_code(code, verifier)          (back channel)
      3. verify_id_token(token_response["id_token"]) -> claims
      4. is_new = db.upsert_user(claims["sub"], ...)
         if is_new: db.seed_default_columns(claims["sub"])
      5. request.session["sub"] = claims["sub"] -> redirect to /
      Failures REDIRECT to /?error=<readable message> — the browser is
      mid-navigation, not mid-fetch, so JSON errors would strand the user.

  POST /auth/logout    Task 4.2
      request.session.clear() -> redirect to /


def get_current_user(request) -> dict:     Task 4.3
    The dependency every /api route declares. Read sub from request.session,
    db.get_user(sub); missing either -> raise HTTPException(401).
    Why a dependency (not middleware): routes declare their own auth need,
    and tests swap it out via app.dependency_overrides (Task 5.4).
"""

# TODO(Task 4.2): router + the three routes
# TODO(Task 4.3): get_current_user
