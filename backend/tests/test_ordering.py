"""Tests for ordering.reorder — YOUR CODE, Task 5.1 (write these FIRST).

The interesting inputs (from the plan's Task 5 discussion). One test each;
name every test after the behavior, not the mechanics.
"""

# TODO(Task 5.1) — write these before ordering.py exists, run pytest, watch
# them fail for the RIGHT reason (ModuleNotFoundError / NotImplementedError):
#
#   test_move_forward_within_list        e.g. [a,b,c,d]: move a to index 2
#   test_move_backward_within_list       e.g. [a,b,c,d]: move d to index 0
#   test_move_to_same_position_is_noop
#   test_target_index_past_end_clamps    move a to index 99 -> lands at end
#   test_moved_id_not_in_list_inserts    the cross-column case: [a,b] + z at 1
#   test_returns_new_list_input_unchanged  (purity — no mutation of the input)
