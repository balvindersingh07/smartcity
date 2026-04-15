# Phase 2 to Phase 10 Implementation Notes

## Phase 2: Service Skeletons

- FastAPI service scaffold for ingestion, processing, storage, api, notification.
- Dockerfiles for each service.
- Local orchestration in `docker-compose.yml`.

## Phase 3: Kafka Integration

- Ingestion publishes to `raw-sensor-data`.
- Processing consumes raw stream and emits:
  - `processed-sensor-data`
  - `sensor-alerts`

## Phase 4: Stream Processing

- Validation rules by metric range.
- Rolling average aggregation by metric type.
- Anomaly detection with threshold-based alerts.

## Phase 5: Database Design

- PostgreSQL metadata tables:
  - `locations`
  - `sensors`
- Time-series simulation table:
  - `sensor_data` (indexed, append-only pattern)

## Phase 6: API Service

- Endpoints:
  - `/metrics`
  - `/sensors`
  - `/alerts`

## Phase 7: Docker + Kubernetes

- Service Dockerfiles optimized using slim runtime images.
- K8s manifests include:
  - Deployments + Services
  - ConfigMap + Secret example
  - HPA

## Phase 8: CI/CD

- GitHub Actions pipeline for test/build and deploy placeholder.

## Phase 9: Terraform

- Simplified Azure stack:
  - Resource Group
  - VNet + subnet
  - AKS cluster
  - PostgreSQL Flexible Server

## Phase 10: Security + Monitoring

- Basic RBAC manifests.
- Env/secret injection pattern.
- Health endpoints in all services.
- Structured logging baseline in Python services.
