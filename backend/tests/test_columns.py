"""Column API tests — YOUR CODE, Task 6.1 (write these FIRST).

Uses the `client` fixture from conftest.py. Five behaviors from the plan:
"""

# TODO(Task 6.1):
#
#   test_board_starts_empty_and_columns_appear_in_order
#       fresh user -> GET /api/board == {"columns": []}
#       two POSTs -> board shows both, positions 0 and 1
#
#   test_rename_persists
#   test_rename_missing_column_404s
#
#   test_other_users_column_is_invisible      <- THE most important test here
#       insert a column for a DIFFERENT user id via db functions directly;
#       PATCH and DELETE it as the logged-in fake user -> 404, row unchanged
#
#   test_delete_removes_column_from_board
#
#   test_unauthenticated_request_401s
#       a TestClient WITHOUT the dependency override -> GET /api/board == 401
