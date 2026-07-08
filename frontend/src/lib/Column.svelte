<script>
  import Card from './Card.svelte'

  let { column, onrename, ondelete, onaddcard, onupdatecard, ondeletecard, onmovecard } =
    $props()

  // Edit-mode plumbing (provided — UI mechanics, not curriculum).
  // The actual persistence goes through the callbacks, which YOU implement
  // in Board.svelte (Task 9).
  let editingTitle = $state(false)
  let draftTitle = $state('')
  let newCardText = $state('')

  function startEditTitle() {
    draftTitle = column.title
    editingTitle = true
  }

  function submitTitle(event) {
    event.preventDefault()
    editingTitle = false
    if (draftTitle.trim() && draftTitle !== column.title) {
      onrename(column.id, draftTitle.trim())
    }
  }

  function submitCard(event) {
    event.preventDefault()
    if (newCardText.trim()) {
      onaddcard(column.id, newCardText.trim())
      newCardText = ''
    }
  }

  // ── YOUR CODE — Task 10: this column as a drop target ────────────────────

  function handleDragOver(event) {
    // TODO(Task 10.1): event.preventDefault() — without it, `drop` NEVER
    // fires. This is THE classic HTML5 drag-and-drop gotcha; the plan says
    // to experience it once (leave this empty, watch drop not fire) before
    // fixing it.
  }

  function handleDrop(event) {
    // TODO(Task 10.1, then 10.3):
    //   v1: read the card id from event.dataTransfer, append to this column:
    //       onmovecard(cardId, column.id, column.cards.length)
    //   v2 (10.3): compute the between-cards index from the hovered card
    //       instead of always appending.
  }
</script>

<section
  class="column"
  role="group"
  aria-label="Column: {column.title}"
  ondragover={handleDragOver}
  ondrop={handleDrop}
>
  <header class="col-head">
    {#if editingTitle}
      <form onsubmit={submitTitle} class="title-form">
        <!-- svelte-ignore a11y_autofocus -->
        <input type="text" bind:value={draftTitle} autofocus onblur={submitTitle} />
      </form>
    {:else}
      <button class="col-title" onclick={startEditTitle} title="Rename column">
        {column.title}
      </button>
    {/if}
    <span class="count">{column.cards.length}</span>
    <button
      class="col-delete"
      onclick={() => ondelete(column.id)}
      title="Delete column (and its cards)"
      aria-label="Delete column {column.title}"
    >
      ×
    </button>
  </header>

  <ul class="cards">
    {#each column.cards as card (card.id)}
      <Card {card} onupdate={onupdatecard} ondeletecard={ondeletecard} />
    {/each}
  </ul>

  <form class="add-card" onsubmit={submitCard}>
    <input type="text" placeholder="Add a card…" bind:value={newCardText} />
  </form>
</section>

<style>
  .column {
    background: var(--paper-deep);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    width: 272px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    max-height: calc(100vh - 8.5rem);
  }

  .col-head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.65rem 0.75rem 0.35rem;
  }

  .col-title {
    font-family: var(--font-display);
    font-weight: 600;
    font-size: 1.02rem;
    text-align: left;
    flex: 1;
    padding: 0.1rem 0.3rem;
    border-radius: var(--radius-sm);
    min-width: 0;
    overflow-wrap: anywhere;
  }

  .col-title:hover {
    background: color-mix(in srgb, var(--surface) 70%, transparent);
  }

  .title-form {
    flex: 1;
  }

  .title-form input {
    width: 100%;
    font-family: var(--font-display);
    font-weight: 600;
  }

  .count {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--ink-soft);
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0.05rem 0.5rem;
  }

  .col-delete {
    color: var(--ink-faint);
    font-size: 1.1rem;
    line-height: 1;
    padding: 0.15rem 0.35rem;
    border-radius: var(--radius-sm);
    transition: color 120ms ease, background 120ms ease;
  }

  .col-delete:hover {
    color: var(--accent-deep);
    background: var(--accent-wash);
  }

  .cards {
    list-style: none;
    margin: 0;
    padding: 0.35rem 0.6rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    overflow-y: auto;
    flex: 1;
    min-height: 2.25rem; /* still a drop target when empty */
  }

  .add-card {
    padding: 0.35rem 0.6rem 0.6rem;
  }

  .add-card input {
    width: 100%;
    background: transparent;
    border-color: transparent;
    font-size: 0.9rem;
  }

  .add-card input:hover {
    background: color-mix(in srgb, var(--surface) 70%, transparent);
  }

  .add-card input:focus {
    background: var(--surface);
  }
</style>
