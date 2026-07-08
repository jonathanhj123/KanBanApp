"""App wiring — YOUR CODE, Tasks 1.4 and 2.3.

What lives here (and only this — keep it thin, like GoogleOAuthProject's main.py):
  - the FastAPI() instance
  - SessionMiddleware, signed with settings.session_secret
  - a lifespan handler that calls db.create_tables() on startup   (Task 2.3)
  - GET /api/health  ->  {"status": "ok"}                          (Task 1.4)
  - include the routers:  auth.router (Task 4), api.router (Task 6)

Run with:  python -m uvicorn main:app --reload --port 8001
"""

# TODO(Task 1.4): app + SessionMiddleware + /api/health
# TODO(Task 2.3): lifespan -> db.create_tables()
# TODO(Task 4.2): app.include_router(auth.router)
# TODO(Task 6.2): app.include_router(api.router)
