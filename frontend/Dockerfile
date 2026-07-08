# Dev image for the Svelte frontend (Vite dev server, not a production build).
# Same split as the backend image: npm dependencies live in the image, source
# code is bind-mounted, so edits hot-reload without a rebuild.
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
