import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'

// THE load-bearing piece of the whole SPA + session-cookie design (plan Task 8):
// the browser only ever talks to :5173, and Vite forwards /api and /auth to the
// backend. Result: the session cookie is first-party — no CORS, no SameSite pain.
//
// Bare metal: the backend is on localhost. In Docker, containers reach each other
// by service name, so compose sets BACKEND_ORIGIN=http://backend:8001.
const backendOrigin = process.env.BACKEND_ORIGIN ?? 'http://localhost:8001'

export default defineConfig({
  plugins: [svelte()],
  server: {
    host: true, // listen on 0.0.0.0 so the container port-mapping works
    proxy: {
      '/api': backendOrigin,
      '/auth': backendOrigin,
    },
    // Bind-mounted files on Windows/Docker don't emit change events; polling
    // restores hot reload. Only needed inside the container.
    watch: { usePolling: Boolean(process.env.BACKEND_ORIGIN) },
  },
})
