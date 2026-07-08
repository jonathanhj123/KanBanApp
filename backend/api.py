"""Board API — YOUR CODE, Tasks 6 and 7.

router = APIRouter(prefix="/api")
Every route takes  user: dict = Depends(auth.get_current_user).
db returned None/False -> raise HTTPException(404) (never 403 — don't leak existence).

Routes and shapes (the frontend stubs already call exactly these):

  GET    /api/me            -> {id, name, email, picture}            Task 6
  GET    /api/board         -> {"columns": db.get_board(user["id"])} Task 6
  POST   /api/columns       body {"title": str}          -> 201 + column   Task 6
  PATCH  /api/columns/{id}  body {"title": str}          -> column         Task 6
  DELETE /api/columns/{id}                               -> 204            Task 6
  POST   /api/cards         body {"column_id","text"}    -> 201 + card     Task 7
  PATCH  /api/cards/{id}    body {"text"} OR {"column_id","position"}      Task 7
  DELETE /api/cards/{id}                                 -> 204            Task 7

Pydantic request models give you the 422s for free; the PATCH-with-two-shapes
model is a discussion point in plan Task 7 before you write it.
"""

# TODO(Task 6.2): router, /api/me, /api/board, column routes
# TODO(Task 7.2): card routes
