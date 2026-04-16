# Smart City Environmental Monitoring System

Production-style distributed system scaffold for real-time environmental monitoring.

## Tech Stack

- Microservices: Python + FastAPI
- Streaming: Apache Kafka
- Databases: PostgreSQL (metadata) + time-series simulation (`sensor_data` table)
- Containerization: Docker + Docker Compose
- Orchestration: Kubernetes (AKS-ready manifests)
- IaC: Terraform (Azure-oriented baseline)
- CI/CD: GitHub Actions

## Repository Layout

```text
smart-city/
├── services/
│   ├── ingestion-service/
│   ├── processing-service/
│   ├── storage-service/
│   ├── api-service/
│   └── notification-service/
├── kafka/
├── kubernetes/
├── terraform/
├── ci-cd/
└── frontend-react/
```

## Phase Deliverables

1. Architecture and requirements: covered in the submitted project report
2. Service skeletons + Dockerfiles: `services/*`
3. Kafka integration + event contracts: `kafka/` and service code
4. Stream processing (filter, aggregate, anomaly): `processing-service/app/pipeline.py`
5. Database schema + ORM: `storage-service/app/models.py`
6. API service (`/metrics`, `/sensors`, `/alerts`): `api-service/app/main.py`
7. Kubernetes manifests: `kubernetes/`
8. CI/CD pipelines: `.github/workflows/ci-cd.yml` and `ci-cd/`
9. Terraform baseline: `terraform/`
10. Security + monitoring hooks: health endpoints, env secrets, RBAC manifests
11. Production hardening: retries/backoff, DLQ, Prometheus metrics, Alembic, React starter

## Quick Start (Local)

```bash
docker compose up --build
```

Services:

- Ingestion: `http://localhost:8001/docs`
- Processing: `http://localhost:8002/docs`
- Storage: `http://localhost:8003/docs`
- API: `http://localhost:8004/docs`
- Notification: `http://localhost:8005/docs`

Prometheus endpoints:

- Ingestion: `http://localhost:8001/metrics/prometheus`
- Processing: `http://localhost:8002/metrics/prometheus`
- Storage: `http://localhost:8003/metrics/prometheus`
- API: `http://localhost:8004/metrics/prometheus`
- Notification: `http://localhost:8005/metrics/prometheus`

## Migrations

```bash
cd services/storage-service
alembic upgrade head
```

## React Frontend Starter

```bash
cd frontend-react
npm install
npm run dev
```

## Example Ingest Request

```bash
curl -X POST http://localhost:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_id":"sensor-001",
    "type":"temperature",
    "value":31.5,
    "timestamp":"2026-04-15T10:00:00Z",
    "location_id":"zone-a"
  }'
```
