<script>
  let { card, onupdate, ondeletecard } = $props()

  // Inline-edit plumbing (provided). Persistence goes through onupdate,
  // which YOU implement in Board.svelte (Task 9.2).
  let editing = $state(false)
  let draft = $state('')

  function startEdit() {
    draft = card.text
    editing = true
  }

  function submitEdit(event) {
    event.preventDefault()
    editing = false
    if (draft.trim() && draft !== card.text) {
      onupdate(card.id, draft.trim())
    }
  }

  // ── YOUR CODE — Task 10.1: make this card draggable ──────────────────────

  function handleDragStart(event) {
    // TODO(Task 10.1): stash the card id for the drop target to read:
    //   event.dataTransfer.setData('text/plain', card.id)
    //   event.dataTransfer.effectAllowed = 'move'
  }
</script>

<li class="card" draggable="true" ondragstart={handleDragStart}>
  {#if editing}
    <form onsubmit={submitEdit}>
      <!-- svelte-ignore a11y_autofocus -->
      <input type="text" bind:value={draft} autofocus onblur={submitEdit} />
    </form>
  {:else}
    <button class="card-text" onclick={startEdit} title="Edit card">
      {card.text}
    </button>
    <button
      class="card-delete"
      onclick={() => ondeletecard(card.id)}
      aria-label="Delete card"
      title="Delete card"
    >
      ×
    </button>
  {/if}
</li>

<style>
  .card {
    position: relative;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--radius-sm);
    box-shadow: var(--shadow-card);
    cursor: grab;
    transition: transform 120ms ease, box-shadow 120ms ease;
  }

  .card:hover {
    transform: translateY(-1px);
    box-shadow: var(--shadow-lift);
  }

  .card:active {
    cursor: grabbing;
  }

  /* The browser's drag ghost picks this up nicely: a slight tilt reads as
     "picked up off the paper". */
  .card:global(.dragging) {
    transform: rotate(2.5deg);
    opacity: 0.85;
  }

  .card-text {
    display: block;
    width: 100%;
    text-align: left;
    font-size: 0.9rem;
    padding: 0.55rem 1.6rem 0.55rem 0.7rem;
    overflow-wrap: anywhere;
  }

  .card-delete {
    position: absolute;
    top: 0.3rem;
    right: 0.3rem;
    color: var(--ink-faint);
    font-size: 0.95rem;
    line-height: 1;
    padding: 0.1rem 0.3rem;
    border-radius: 4px;
    opacity: 0;
    transition: opacity 120ms ease, color 120ms ease, background 120ms ease;
  }

  .card:hover .card-delete,
  .card-delete:focus-visible {
    opacity: 1;
  }

  .card-delete:hover {
    color: var(--accent-deep);
    background: var(--accent-wash);
  }

  .card form {
    padding: 0.3rem;
  }

  .card input {
    width: 100%;
    font-size: 0.9rem;
  }
</style>
