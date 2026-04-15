# Phase 11: Production Hardening

This phase adds reliability, observability, migration discipline, and a modern frontend entry point.

## Implemented Upgrades

1. **Retry/Backoff**
   - Kafka publish operations now use bounded retry with exponential backoff.
   - Downstream HTTP calls in API service include retries and timeout handling.

2. **Dead-Letter Queue (DLQ)**
   - Invalid events from processing flow are routed to `sensor-dlq`.
   - DLQ helps isolate malformed/out-of-range data from the main stream.

3. **Prometheus Metrics**
   - Service-level counters/histograms exposed at `/metrics/prometheus`.
   - Useful for scraping by Prometheus and visualization in Grafana.

4. **Alembic Migrations**
   - Storage service includes Alembic scaffold and initial migration.
   - Supports controlled DB schema evolution.

5. **React Frontend Starter**
   - Added Vite + React app (`frontend-react`) consuming `/metrics`, `/sensors`, `/alerts`.
   - Designed as upgrade path from static dashboard.
