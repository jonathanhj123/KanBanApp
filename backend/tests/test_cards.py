"""Card API tests — YOUR CODE, Task 7.1 (write these FIRST).

The behaviors from the plan. After every move, assert via GET /api/board that
positions are contiguous 0..n-1 — that's the renumbering contract.
"""

# TODO(Task 7.1):
#
#   test_new_cards_append_with_contiguous_positions   (three creates -> 0,1,2)
#   test_edit_card_text_persists
#   test_move_within_column                (position 2 -> 0; order + contiguity)
#   test_move_across_columns               (source renumbered, target ordered,
#                                           card's column_id changed)
#   test_move_to_foreign_column_404s_and_changes_nothing
#   test_foreign_card_edit_delete_404      (the JOIN-scoping test)
#   test_delete_card
#   test_deleting_column_cascades_to_cards (CASCADE proven through the API)
