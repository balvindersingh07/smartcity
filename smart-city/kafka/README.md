# Kafka Integration Notes

## Topics

- `raw-sensor-data` (produced by ingestion-service)
- `processed-sensor-data` (produced by processing-service)
- `sensor-alerts` (produced by processing-service, consumed by notification-service)

## Message Contract

See `message-schema.json`.

## Local Validation Flow

1. Start stack: `docker compose up --build`
2. Send sample event to ingestion-service (`/ingest`)
3. Check:
   - `processing-service /aggregates`
   - `storage-service /metrics`
   - `notification-service /alerts`
