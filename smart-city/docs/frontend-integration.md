# Frontend Integration (Existing Dashboard)

The existing dashboard (`/app.js`) now attempts to fetch live data from:

- `GET http://localhost:8004/metrics`
- `GET http://localhost:8004/sensors`
- `GET http://localhost:8004/alerts`

If backend services are unavailable, it falls back to simulated local data.

## Optional Override

Set a custom API base URL before `app.js` loads:

```html
<script>
  window.SMART_CITY_API_BASE = "http://your-api-host:8004";
</script>
```
