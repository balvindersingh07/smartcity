# Phase 1: Architecture, Requirements, and Communication Design

## 1) Functional Requirements

- Ingest IoT events for air quality, temperature, humidity, and noise.
- Stream data reliably with ordered/event-driven flow through Kafka topics.
- Validate and process streams in near real-time.
- Store metadata (`sensors`, `locations`) and time-series sensor data.
- Expose dashboard APIs for metrics, sensors, and alerts.
- Generate threshold/anomaly alerts for operations teams.

## 2) Non-Functional Requirements

- Scalability: horizontally scale stateless services and consumers.
- Availability: health checks and restart-safe deployment design.
- Reliability: at-least-once delivery using Kafka consumer groups.
- Observability: structured logs, health/readiness endpoints, metrics hooks.
- Security: secret-by-env pattern, least-privilege service accounts.
- Latency target: sub-second ingest acknowledgement, low-second dashboard freshness.

## 3) Text-Based Architecture Diagram

```text
IoT Sensors / Gateways
        |
        | REST (JSON events)
        v
[ingestion-service] ----produce----> Kafka topic: raw-sensor-data
                                        |
                                        | consume
                                        v
                                  [processing-service]
                                      | filter/aggregate/anomaly
                                      | produce processed
                                      v
                          Kafka topic: processed-sensor-data
                                      |
                                      | consume
                                      v
                                [storage-service]
                               /                  \
                              v                    v
                     PostgreSQL (metadata)   sensor_data (time-series simulation)

[notification-service] <---- consume anomalies topic ---- [processing-service]
        |
        v
   Alerts state/API

[api-service] ---REST---> storage-service + notification-service
        |
        v
  Dashboard / Frontend
```

## 4) Communication Model

### Synchronous (REST)

- Dashboard -> API service
- API service -> storage service / notification service
- IoT producer -> ingestion service

### Asynchronous (Kafka)

- ingestion-service -> `raw-sensor-data`
- processing-service consumes `raw-sensor-data`
- processing-service -> `processed-sensor-data` and `sensor-alerts`
- storage-service consumes `processed-sensor-data`
- notification-service consumes `sensor-alerts`

## 5) Event Contract

```json
{
  "sensor_id": "sensor-001",
  "type": "temperature",
  "value": 31.5,
  "timestamp": "2026-04-15T10:00:00Z",
  "location_id": "zone-a"
}
```

Processed event enriches with validation and aggregate context:

```json
{
  "sensor_id": "sensor-001",
  "type": "temperature",
  "value": 31.5,
  "timestamp": "2026-04-15T10:00:00Z",
  "location_id": "zone-a",
  "is_valid": true,
  "rolling_avg": 29.8
}
```
