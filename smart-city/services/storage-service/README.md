# Storage Service

## Responsibilities

- Consume processed sensor stream from Kafka.
- Persist metadata (`locations`, `sensors`) and time-series data (`sensor_data`) in PostgreSQL.
- Serve metrics and sensor APIs to upstream API service.

## Migrations (Alembic)

```bash
cd smart-city/services/storage-service
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "describe_change"
```
