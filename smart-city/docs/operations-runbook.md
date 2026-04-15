# Operations Runbook

## Local Recovery Commands

```bash
docker compose -f smart-city/docker-compose.yml up -d --build
docker compose -f smart-city/docker-compose.yml ps
docker compose -f smart-city/docker-compose.yml logs -f api-service
```

## Health Verification

- Ingestion: `/health`
- Processing: `/health`
- Storage: `/health`
- API: `/health`
- Notification: `/health`

Prometheus endpoints: `/metrics/prometheus`

## Incident: API returns empty metrics

1. Check storage service logs:
   ```bash
   docker compose -f smart-city/docker-compose.yml logs storage-service --tail 100
   ```
2. Check processing service is producing:
   ```bash
   docker compose -f smart-city/docker-compose.yml logs processing-service --tail 100
   ```
3. Re-send a test event to ingestion.
4. Re-check `/metrics` and `/sensors`.

## Incident: Kafka unavailable

1. Confirm kafka and zookeeper containers are up.
2. Restart dependent services:
   ```bash
   docker compose -f smart-city/docker-compose.yml restart ingestion-service processing-service storage-service notification-service
   ```

## Incident: Staging deploy failed

1. Review GitHub Actions logs.
2. Re-run `ci-cd/smoke-test.ps1`.
3. Rollback by applying previous image tag in deployment manifests.
