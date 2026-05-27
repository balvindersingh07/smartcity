# Smart City Dashboard (static frontend)

Premium environmental monitoring UI: map, charts, metrics, alerts, and sensor table.

## Run locally

Backend must be running first (`docker compose up -d` from `smart-city/`).

```bash
cd smart-city/frontend-react
npm install
npm run dev
```

Open the URL shown in the terminal (default `http://localhost:5173`).

On `localhost`, the dashboard calls **`http://localhost:8004`**. On other hosts it uses the staging API URL set in `index.html`.

## Build

```bash
npm run build
npm run preview
```

Output: `dist/`

## Deploy on Vercel

1. Import this Git repo on [Vercel](https://vercel.com).
2. **Root Directory:** `smart-city/frontend-react`
3. **Build:** `npm run build` — **Output:** `dist`
4. Edit the non-local API URL in `index.html` if your API host changes.

The API must be reachable from the browser (HTTPS in production). CORS on `api-service` allows `*`.
