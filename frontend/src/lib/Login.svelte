<script>
  // Presentational only — no logic for you to write here.
  // The button is a real navigation (<a>), NOT a fetch: the OAuth flow is a
  // chain of browser redirects, and cookies ride along at navigation level.
  let { error = null } = $props()
</script>

<main class="login">
  <div class="deco" aria-hidden="true">
    <div class="deco-col">
      <span class="deco-card w7"></span>
      <span class="deco-card w5"></span>
      <span class="deco-card w6"></span>
    </div>
    <div class="deco-col">
      <span class="deco-card w5 hot"></span>
      <span class="deco-card w7"></span>
    </div>
    <div class="deco-col">
      <span class="deco-card w6"></span>
    </div>
  </div>

  <section class="panel">
    <p class="kicker">A learning project, hand-rolled</p>
    <h1>Your board is<br /><em>waiting.</em></h1>
    <p class="sub">
      Columns, cards, drag-and-drop — behind a Google sign-in you built from
      the raw protocol up.
    </p>

    {#if error}
      <div class="error" role="alert">
        <strong>Sign-in didn’t finish:</strong>
        {error}
      </div>
    {/if}

    <a class="google-btn" href="/auth/login">
      <svg viewBox="0 0 48 48" width="20" height="20" aria-hidden="true">
        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z" />
        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z" />
        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z" />
        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z" />
      </svg>
      Continue with Google
    </a>

    <p class="fine">
      The whole flow — <code>state</code>, PKCE, token exchange, JWKS
      verification — lives in <code>backend/oauth.py</code> and
      <code>backend/tokens.py</code>. You wrote it. Well… you will.
    </p>
  </section>
</main>

<style>
  .login {
    flex: 1;
    display: grid;
    place-items: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;
  }

  /* Ghost of a kanban board floating behind the panel */
  .deco {
    position: absolute;
    inset: 0;
    display: flex;
    gap: 2.5rem;
    justify-content: center;
    align-items: center;
    transform: rotate(-8deg) scale(1.15);
    opacity: 0.5;
  }

  .deco-col {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
  }

  .deco-card {
    display: block;
    height: 44px;
    border-radius: 8px;
    background: var(--paper-deep);
    border: 1px solid var(--line);
  }

  .deco-card.hot {
    background: var(--accent-wash);
    border-color: color-mix(in srgb, var(--accent) 35%, var(--line));
  }

  .w5 { width: 130px; }
  .w6 { width: 160px; }
  .w7 { width: 190px; }

  .panel {
    position: relative;
    max-width: 26rem;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 2.5rem 2.5rem 2rem;
    box-shadow: var(--shadow-lift);
    text-align: center;
    animation: rise 500ms cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }

  @keyframes rise {
    from {
      opacity: 0;
      transform: translateY(14px);
    }
  }

  .kicker {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--accent-deep);
    margin: 0 0 0.75rem;
  }

  h1 {
    font-size: 2.4rem;
    line-height: 1.05;
  }

  h1 em {
    font-style: italic;
    color: var(--accent);
  }

  .sub {
    color: var(--ink-soft);
    margin: 1rem 0 1.5rem;
  }

  .error {
    background: var(--accent-wash);
    border: 1px solid color-mix(in srgb, var(--accent) 40%, var(--line));
    border-radius: var(--radius-sm);
    color: var(--accent-deep);
    font-size: 0.88rem;
    padding: 0.6rem 0.8rem;
    margin-bottom: 1.25rem;
    text-align: left;
  }

  .google-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    background: var(--ink);
    color: var(--surface);
    text-decoration: none;
    font-weight: 700;
    padding: 0.75rem 1.4rem;
    border-radius: 999px;
    transition: transform 120ms ease, box-shadow 120ms ease;
    box-shadow: var(--shadow-card);
  }

  .google-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lift);
  }

  .google-btn svg {
    background: #fff;
    border-radius: 50%;
    padding: 2px;
  }

  .fine {
    margin: 1.5rem 0 0;
    font-size: 0.78rem;
    color: var(--ink-faint);
  }

  .fine code {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    background: var(--paper);
    padding: 0.1em 0.35em;
    border-radius: 4px;
  }
</style>
