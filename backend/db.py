"""All SQL lives here — YOUR CODE, Tasks 2, 4, 6, 7.

Rules that apply to every function in this file (see plan: Global Constraints):
  - parameterized queries only (%s placeholders) — never f-strings/format
  - every query is scoped to the logged-in user; cards are reached only by
    JOINing through columns.user_id (cards have no user_id of their own)
  - "exists but isn't yours" must be indistinguishable from "doesn't exist":
    return None/False and let the route turn that into a 404
"""

# ── Task 2: connection + schema ────────────────────────────────────────────


def get_connection():
    """Return a new psycopg2 connection using settings.database_url."""
    raise NotImplementedError  # TODO(Task 2.2)


def create_tables():
    """Create users / columns / cards if they don't exist (idempotent).

    Copy the schema from the spec (docs/superpowers/specs/...), don't retype
    from memory — schema drift between doc and DB is a classic bug class.
    """
    raise NotImplementedError  # TODO(Task 2.2)


# ── Task 4: users ───────────────────────────────────────────────────────────


def upsert_user(sub, email, name, picture):
    """INSERT ... ON CONFLICT (id) DO UPDATE. Key = Google's `sub`, never email.

    Returns True if the user was NEWLY created (caller seeds default columns),
    False if they already existed. Upsert + seed happen in one transaction.
    """
    raise NotImplementedError  # TODO(Task 4.1)


def get_user(user_id):
    """Return the user row as a dict {id, email, name, picture}, or None."""
    raise NotImplementedError  # TODO(Task 4.1)


def seed_default_columns(user_id):
    """Insert 'To Do' / 'Doing' / 'Done' at positions 0, 1, 2."""
    raise NotImplementedError  # TODO(Task 4.1)


# ── Task 6: columns + board read ───────────────────────────────────────────


def get_board(user_id):
    """All of the user's columns (by position), each with nested cards (by position).

    Two queries assembled in Python (see plan Task 6 for why not one JOIN):
      1) my columns   2) all cards JOINed through my columns
    Returns: [{id, title, position, cards: [{id, text, position}, ...]}, ...]
    """
    raise NotImplementedError  # TODO(Task 6.2)


def create_column(user_id, title):
    """Insert at position = max(position)+1 among MY columns. Returns the new column dict."""
    raise NotImplementedError  # TODO(Task 6.2)


def rename_column(user_id, column_id, title):
    """Returns the updated column dict, or None if not found / not mine."""
    raise NotImplementedError  # TODO(Task 6.2)


def delete_column(user_id, column_id):
    """Returns True if deleted, False if not found / not mine. Cards go via CASCADE."""
    raise NotImplementedError  # TODO(Task 6.2)


# ── Task 7: cards ───────────────────────────────────────────────────────────


def create_card(user_id, column_id, text):
    """Position = end of column. Returns new card dict, or None if the column isn't mine."""
    raise NotImplementedError  # TODO(Task 7.2)


def update_card_text(user_id, card_id, text):
    """Returns updated card dict, or None. Ownership check = JOIN through columns."""
    raise NotImplementedError  # TODO(Task 7.2)


def move_card(user_id, card_id, new_column_id, new_position):
    """The hard one. ONE transaction:
      load target column's ordered card ids -> ordering.reorder(...) ->
      UPDATE positions (+ the moved card's column_id) ->
      if the card changed columns, renumber the source column too -> commit.
    Returns True, or False if card/target column isn't mine (nothing changed).
    """
    raise NotImplementedError  # TODO(Task 7.2)


def delete_card(user_id, card_id):
    """Returns True if deleted, False if not found / not mine."""
    raise NotImplementedError  # TODO(Task 7.2)
