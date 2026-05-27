# Database Design

## Overview

Sensor **metadata** and **time-series readings** are stored in **PostgreSQL**. The schema is optimized for write-heavy ingest (Kafka consumer batch commits) and read patterns for dashboard aggregates (latest value, averages by metric type).

**Implementation:** `smart-city/services/storage-service/app/models.py`  
**Migrations:** `smart-city/services/storage-service/alembic/` (if present) or SQLAlchemy `create_all` on startup

---

## Entity-relationship model

```
locations (1) ──< (N) sensors (1) ──< (N) sensor_data
```

| Table | Purpose |
|-------|---------|
| `locations` | City zones / geographic areas |
| `sensors` | IoT device registry (id, type, location, status) |
| `sensor_data` | Time-series readings (value, rolling_avg, validity, timestamp) |

---

## Table definitions

### `locations`

| Column | Type | Notes |
|--------|------|-------|
| `id` | VARCHAR(64) PK | Zone identifier |
| `name` | VARCHAR(128) | Display name |
| `city` | VARCHAR(128) | City name |

### `sensors`

| Column | Type | Notes |
|--------|------|-------|
| `id` | VARCHAR(64) PK | Sensor identifier |
| `type` | VARCHAR(32) | temperature, humidity, aqi, noise |
| `location_id` | FK → locations.id | Zone assignment |
| `status` | VARCHAR(24) | active / inactive |

### `sensor_data`

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER PK | Auto-increment |
| `sensor_id` | FK → sensors.id | Indexed |
| `type` | VARCHAR(32) | Indexed for aggregate queries |
| `value` | FLOAT | Raw reading |
| `rolling_avg` | FLOAT NULL | From stream processor |
| `is_valid` | BOOLEAN | Validation flag |
| `recorded_at` | TIMESTAMP | Indexed for time-range queries |

---

## Write path

1. `processing-service` publishes validated event to Kafka `processed-sensor-data`  
2. `storage-service` consumer inserts row into `sensor_data`  
3. Auto-creates `sensor` and `location` if missing (demo-friendly)

---

## Read path (API / dashboard)

`storage-service` `/metrics` executes:

- `AVG(value)` per metric type where `is_valid = true`  
- Latest reading per type (`ORDER BY recorded_at DESC LIMIT 1`)

`api-service` proxies these endpoints to the dashboard.

---

## Indexing strategy

- `sensor_data.sensor_id` — filter by device  
- `sensor_data.type` — aggregate by metric  
- `sensor_data.recorded_at` — time-series queries  

---

## Azure provisioning

Terraform creates **Azure Database for PostgreSQL Flexible Server** (`smart-city/terraform/main.tf`). Connection string injected via Kubernetes secrets.

---

## Capstone brief alignment

| Brief | This design |
|-------|-------------|
| Relational DB for metadata | `locations`, `sensors` |
| Time-series store | `sensor_data` with timestamp index |
| Write-heavy workload | Async Kafka consumer, single-row inserts |
| Azure SQL | PostgreSQL (Azure-managed equivalent) |
