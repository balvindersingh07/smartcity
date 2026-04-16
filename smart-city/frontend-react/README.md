# Frontend React (Vite)

## Run locally

```bash
cd smart-city/frontend-react
npm install
npm run dev
```

## API base URL

Default: `http://localhost:8004` (see `src/App.jsx`).

Override (PowerShell):

```powershell
$env:VITE_SMART_CITY_API_BASE="http://localhost:8004"; npm run dev
```

Copy `.env.example` to `.env` and set `VITE_SMART_CITY_API_BASE` if you prefer a file.

## Deploy on Vercel

1. Import this Git repo on [Vercel](https://vercel.com).
2. **Root Directory:** `smart-city/frontend-react`
3. **Build:** `npm run build` — **Output:** `dist`
4. **Environment variable:** `VITE_SMART_CITY_API_BASE` = your public **HTTPS** API URL (no trailing slash).

The API must be reachable with HTTPS from the browser. CORS on `api-service` is open (`*`); you can narrow it later.
