<script>
  import Column from './Column.svelte'
  // import { apiFetch } from './api.js'

  // Single source of truth: Board owns the whole board object; children get
  // data + callbacks as props (same pattern as ToDoListApp's App.svelte).
  let board = $state({ columns: [] })
  let newColumnTitle = $state('')

  // ── YOUR CODE — Tasks 9 and 10. The markup below already calls all of
  //    these with the right arguments; you fill in the bodies. ─────────────

  async function loadBoard() {
    // TODO(Task 9.1): board = await apiFetch('/api/board')
    // Call it once on startup too — $effect(() => { loadBoard() }) or an
    // immediately-invoked async — discuss the options before picking.
  }

  async function addColumn(event) {
    event.preventDefault()
    // TODO(Task 9.1): POST /api/columns { title: newColumnTitle },
    // clear newColumnTitle, then loadBoard(). (Refetch-after-mutate first;
    // optimistic updates arrive with drag-and-drop in Task 10.)
  }

  async function renameColumn(columnId, title) {
    // TODO(Task 9.2): PATCH /api/columns/{columnId} { title }, loadBoard()
  }

  async function deleteColumn(columnId) {
    // TODO(Task 9.2): DELETE /api/columns/{columnId}, loadBoard()
  }

  async function addCard(columnId, text) {
    // TODO(Task 9.2): POST /api/cards { column_id: columnId, text }, loadBoard()
  }

  async function updateCardText(cardId, text) {
    // TODO(Task 9.2): PATCH /api/cards/{cardId} { text }, loadBoard()
  }

  async function deleteCard(cardId) {
    // TODO(Task 9.2): DELETE /api/cards/{cardId}, loadBoard()
  }

  async function moveCard(cardId, columnId, position) {
    // TODO(Task 10.1): the optimistic one — snapshot board, mutate locally,
    // PATCH /api/cards/{cardId} { column_id, position }; on failure restore
    // the snapshot and surface a message. See plan Task 10.
  }
</script>

<main class="board-scroll">
  <div class="board">
    {#each board.columns as column (column.id)}
      <Column
        {column}
        onrename={renameColumn}
        ondelete={deleteColumn}
        onaddcard={addCard}
        onupdatecard={updateCardText}
        ondeletecard={deleteCard}
        onmovecard={moveCard}
      />
    {/each}

    <form class="add-column" onsubmit={addColumn}>
      <input
        type="text"
        placeholder="New column…"
        bind:value={newColumnTitle}
        aria-label="New column title"
      />
      <button type="submit" class="add-btn" disabled={!newColumnTitle.trim()}>
        Add
      </button>
    </form>
  </div>

  {#if board.columns.length === 0}
    <div class="empty">
      <h2>Nothing on the board.</h2>
      <p>
        Either you haven’t implemented <code>loadBoard()</code> yet
        <span class="mono">(Task 9.1)</span> — or you have, and it’s time to
        add your first column. One of these is more likely.
      </p>
    </div>
  {/if}
</main>

<style>
  .board-scroll {
    flex: 1;
    overflow-x: auto;
    overflow-y: hidden;
  }

  .board {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1.5rem;
    min-height: 100%;
  }

  .add-column {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    background: color-mix(in srgb, var(--surface) 55%, transparent);
    border: 1.5px dashed var(--line);
    border-radius: var(--radius);
    min-width: 220px;
  }

  .add-column input {
    flex: 1;
    background: transparent;
    border-color: transparent;
  }

  .add-column input:focus {
    background: var(--surface);
  }

  .add-btn {
    font-family: var(--font-mono);
    font-size: 0.85rem;
    background: var(--accent);
    color: #fff;
    border-radius: var(--radius-sm);
    padding: 0.4rem 0.9rem;
    transition: background 120ms ease;
  }

  .add-btn:hover:not(:disabled) {
    background: var(--accent-deep);
  }

  .add-btn:disabled {
    opacity: 0.4;
    cursor: default;
  }

  .empty {
    max-width: 24rem;
    margin: 12vh auto 0;
    text-align: center;
    color: var(--ink-soft);
  }

  .empty h2 {
    font-size: 1.6rem;
    color: var(--ink);
    margin-bottom: 0.5rem;
  }

  .empty code {
    font-family: var(--font-mono);
    font-size: 0.85em;
    background: var(--paper-deep);
    padding: 0.1em 0.35em;
    border-radius: 4px;
  }

  .mono {
    font-family: var(--font-mono);
    font-size: 0.8em;
    color: var(--ink-faint);
  }
</style>
