# Stream Processing & Messaging

## Message broker

**Apache Kafka** (Confluent locally; Redpanda optional in Kubernetes)

Configuration: `smart-city/docker-compose.yml`, `smart-city/kubernetes/dependencies.yaml`

---

## Topics

| Topic | Producer | Consumer | Purpose |
|-------|----------|----------|---------|
| `raw-sensor-data` | ingestion-service | processing-service | Raw IoT events |
| `processed-sensor-data` | processing-service | storage-service | Validated + enriched events |
| `sensor-alerts` | processing-service | notification-service | Threshold breaches |

Documentation: `smart-city/kafka/README.md`

---

## Message format

JSON schema: `smart-city/kafka/message-schema.json`

**Required fields:**

```json
{
  "sensor_id": "demo-001",
  "type": "temperature",
  "value": 29.5,
  "timestamp": "2026-05-27T12:00:00Z"
}
```

**Optional:** `location_id`

**Allowed types:** `temperature`, `humidity`, `aqi`, `noise`

---

## Processing pipeline

Implementation: `smart-city/services/processing-service/app/pipeline.py`

### Steps

1. **Validation** — value within physical range per metric type  
2. **Rolling average** — sliding window (50 events) per metric type  
3. **Anomaly detection** — compare against thresholds  
4. **Enrichment** — add `processed_at`, `is_valid`, `rolling_avg`  
5. **Alert emission** — publish to `sensor-alerts` if threshold exceeded  

### Thresholds

| Metric | Anomaly threshold |
|--------|-------------------|
| temperature | ≥ 45°C |
| humidity | ≥ 90% |
| aqi | ≥ 150 |
| noise | ≥ 90 dB |

---

## End-to-end flow

```
IoT / curl POST → ingestion-service:8001/ingest
       ↓
  raw-sensor-data (Kafka)
       ↓
  processing-service (validate, aggregate, alert)
       ↓
  processed-sensor-data ──→ storage-service → PostgreSQL
  sensor-alerts         ──→ notification-service → /alerts
       ↓
  api-service:8004/metrics → dashboard
```

Diagram: `docs/images/data-flow.png`

---

## Local test

```bash
cd smart-city && docker compose up -d
```

```bash
curl -X POST http://localhost:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":"demo-001","type":"temperature","value":29.5,"timestamp":"2026-05-27T12:00:00Z"}'
```

Verify:

- http://localhost:8004/metrics  
- http://localhost:8005/alerts  

---

## Capstone brief alignment

| Brief | This implementation |
|-------|---------------------|
| Kafka / RabbitMQ | Apache Kafka |
| Flink / Spark | Python stream processor with stateful rolling windows |
| Real-time filtering & aggregation | validate_event(), StreamState, detect_anomaly() |
