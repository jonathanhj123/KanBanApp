/**
 * The one fetch wrapper every component uses — YOUR CODE, Task 8.2.
 *
 * Contract (Board.svelte and App.svelte already import this):
 *
 *   apiFetch(path, options?) -> parsed JSON (or null for 204 No Content)
 *
 *   - sets  'Content-Type': 'application/json'  when there's a body
 *   - JSON.stringify's  options.body  for the caller
 *   - on a non-2xx response, THROWS an object shaped  { status, message }
 *     so callers can branch on  err.status === 401
 *
 * No credentials config needed — thanks to the Vite proxy the cookie is
 * first-party and the browser attaches it automatically. That's the lesson.
 */

export async function apiFetch(path, options = {}) {
  throw new Error('TODO(Task 8.2): implement apiFetch — see the contract above')
}
