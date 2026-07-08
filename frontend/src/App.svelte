<script>
  import Login from './lib/Login.svelte'
  import Board from './lib/Board.svelte'
  // import { apiFetch } from './lib/api.js'   // you'll need this in Task 8.2

  // ── YOUR CODE — Task 8.2: the session-check state machine ────────────────
  // States: 'loading' → 'loggedIn' | 'loggedOut'
  // Starts at 'loggedOut' so the scaffold renders; when you implement the
  // check, start at 'loading' instead.
  let status = $state('loggedOut')
  let user = $state(null)
  let loginError = $state(null)

  // TODO(Task 8.2): on startup, call apiFetch('/api/me')
  //   success            → user = result; status = 'loggedIn'
  //   err.status === 401 → status = 'loggedOut'
  //   Also read new URLSearchParams(location.search).get('error') into
  //   loginError so OAuth failures surface on the login page.
  //
  // TODO(Task 11.1): expired-session handling — when any later apiFetch
  //   throws a 401, flip status back to 'loggedOut' with a message.
</script>

{#if status === 'loading'}
  <div class="splash" aria-busy="true">
    <span class="splash-mark">🗂️</span>
    <p>Opening your board…</p>
  </div>
{:else if status === 'loggedOut'}
  <Login error={loginError} />
{:else}
  <header class="topbar">
    <span class="brand">KanBan<span class="brand-dot">.</span></span>
    <div class="user-chip">
      {#if user?.picture}
        <img class="avatar" src={user.picture} alt="" referrerpolicy="no-referrer" />
      {/if}
      <span class="user-name">{user?.name ?? user?.email}</span>
      <form method="POST" action="/auth/logout">
        <button class="logout" type="submit">Sign out</button>
      </form>
    </div>
  </header>
  <Board />
{/if}

<style>
  .splash {
    flex: 1;
    display: grid;
    place-content: center;
    justify-items: center;
    gap: 0.75rem;
    color: var(--ink-soft);
  }

  .splash-mark {
    font-size: 2.5rem;
    animation: bob 1.2s ease-in-out infinite;
  }

  @keyframes bob {
    50% {
      transform: translateY(-6px);
    }
  }

  .topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.5rem;
    border-bottom: 1px solid var(--line);
    background: color-mix(in srgb, var(--surface) 75%, transparent);
    backdrop-filter: blur(4px);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .brand {
    font-family: var(--font-display);
    font-style: italic;
    font-weight: 600;
    font-size: 1.35rem;
    letter-spacing: -0.02em;
  }

  .brand-dot {
    color: var(--accent);
    font-style: normal;
  }

  .user-chip {
    display: flex;
    align-items: center;
    gap: 0.6rem;
  }

  .avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    border: 2px solid var(--surface);
    box-shadow: var(--shadow-card);
  }

  .user-name {
    font-size: 0.9rem;
    color: var(--ink-soft);
  }

  .logout {
    font-size: 0.8rem;
    font-family: var(--font-mono);
    color: var(--accent-deep);
    border: 1px solid var(--line);
    border-radius: 999px;
    padding: 0.25rem 0.7rem;
    background: var(--surface);
    transition: border-color 120ms ease, background 120ms ease;
  }

  .logout:hover {
    border-color: var(--accent);
    background: var(--accent-wash);
  }
</style>
