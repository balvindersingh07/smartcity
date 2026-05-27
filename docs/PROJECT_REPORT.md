# Smart City Environmental Monitoring — Project Report

## 1. Executive summary

This capstone implements a **modular distributed system** for real-time environmental monitoring in a smart city. IoT-style sensor events (air quality, noise, temperature, humidity) are ingested through a REST API, streamed via **Apache Kafka**, processed for validation and aggregation, stored in **PostgreSQL**, and exposed through an API consumed by a **web dashboard**.

The system is **containerized with Docker**, orchestrated on **Azure Kubernetes Service (AKS)**, provisioned with **Terraform**, and deployed through **GitHub Actions** CI/CD with staging and production environments.

**Live frontend:** https://smartcity-mocha.vercel.app/  
**Repository:** https://github.com/balvindersingh07/smartcity

---

## 2. Functional requirements

| ID | Requirement | Implementation |
|----|-------------|----------------|
| FR-1 | Ingest sensor data from IoT devices | `ingestion-service` POST `/ingest` → Kafka `raw-sensor-data` |
| FR-2 | Stream processing (filter, aggregate, enrich) | `processing-service` consumes raw topic, validates, rolling average, alerts |
| FR-3 | Persistent storage | `storage-service` → PostgreSQL (`sensors`, `sensor_data`, `locations`) |
| FR-4 | REST API for metrics | `api-service` `/metrics`, `/sensors`, `/alerts` |
| FR-5 | Real-time dashboard | Premium UI in `smart-city/frontend-react`, deployed on Vercel |
| FR-6 | Alerting | `notification-service` consumes `sensor-alerts` topic |

---

## 3. Non-functional requirements

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NFR-1 | Scalability | Kubernetes HPA, stateless microservices |
| NFR-2 | Reliability | Kafka buffering, service restarts, health checks |
| NFR-3 | Security | K8s RBAC, NetworkPolicies, Key Vault (Terraform), secrets |
| NFR-4 | Observability | Prometheus metrics, Azure Application Insights |
| NFR-5 | Cost control | Azure subscription budget alerts (Terraform) |
| NFR-6 | Automation | CI/CD: test → build → GHCR → AKS staging → production |

---

## 4. Architecture overview

### 4.1 Microservices

Five Python/FastAPI services:

1. **Ingestion** (8001) — accepts sensor JSON, publishes to Kafka  
2. **Processing** (8002) — stream validation, rolling averages, anomaly detection  
3. **Storage** (8003) — persists processed events to PostgreSQL  
4. **API** (8004) — aggregates data for dashboard consumers  
5. **Notification** (8005) — alert feed from Kafka  

### 4.2 Diagrams

Insert these PNG files from `docs/images/` into your Word/PDF submission:

- **Microservices:** `architecture-microservices.png`
- **Data flow:** `data-flow.png`
- **Cloud & CI/CD:** `cicd-azure.png`

### 4.3 Communication protocols

- **Synchronous:** REST/HTTP between clients and ingestion/API services  
- **Asynchronous:** Kafka topics (`raw-sensor-data`, `processed-sensor-data`, `sensor-alerts`)

---

## 5. Technology choices vs capstone brief

| Brief recommendation | This project | Rationale |
|---------------------|--------------|-----------|
| Azure SQL | PostgreSQL (Azure Flexible Server via Terraform) | Relational + time-series in one store; Azure-managed option in IaC |
| Azure Data Explorer | PostgreSQL indexed time-series table | Simpler ops for capstone; same query patterns at smaller scale |
| Flink / Spark Streaming | Python Kafka consumer + pipeline | Same event-driven pattern; easier to dockerize and test |
| Azure DevOps / Jenkins | GitHub Actions | Equivalent CI/CD stages; integrated with GHCR |
| Azure Container Registry | GHCR | Container registry with GitHub-native auth |
| React / Angular | HTML/CSS/JS dashboard (Vite build) | Full visualization UI; deployed on Vercel |

Architecture and rubric objectives (microservices, messaging, K8s, IaC, CI/CD, security, monitoring) are met with equivalent tooling.

---

## 6. Deployment topology

- **Local:** Docker Compose (Zookeeper, Kafka, Postgres, all services)  
- **Cloud:** AKS cluster with in-cluster or managed dependencies  
- **Frontend:** Vercel (static build from `smart-city/frontend-react`)  
- **API staging:** Azure load balancer / ingress (see API URL in submission README)

---

## 7. CI/CD pipeline

Workflow: `.github/workflows/ci-cd.yml`

1. Run Python tests per service  
2. Build Docker images  
3. Push to GHCR (`ghcr.io/<owner>/smart-city-<service>:<sha>`)  
4. Deploy to **staging** AKS  
5. Smoke test API endpoints  
6. Deploy to **production** (GitHub Environment approval gate)

Screenshot: `docs/images/screenshot-github-cicd-success-run.png`

Details: `smart-city/ci-cd/README.md`

---

## 8. Infrastructure as Code

Terraform modules provision (see `smart-city/terraform/`):

- Resource group, VNet, AKS  
- PostgreSQL Flexible Server  
- Optional Key Vault, Log Analytics, Application Insights  
- Optional subscription budget alert  

Usage: `smart-city/terraform/README.md`

---

## 9. Security summary

- Kubernetes **RBAC** (`smart-city/kubernetes/rbac.yaml`)  
- **NetworkPolicies** restrict pod-to-pod traffic  
- Secrets via K8s secrets / Key Vault (Terraform)  
- CORS enabled on API for dashboard access  

Details: [SECURITY_AND_MONITORING.md](SECURITY_AND_MONITORING.md)

---

## 10. Monitoring & cost governance

- **Application Insights** linked to AKS (Terraform, optional)  
- **Prometheus** metrics on services (`/metrics/prometheus`)  
- **Azure budget alerts** for cost thresholds  

Screenshots: `screenshot-azure-application-insights-staging.png`, `screenshot-azure-monthly-budget.png`

Details: [SECURITY_AND_MONITORING.md](SECURITY_AND_MONITORING.md), [COST_ANALYSIS.md](COST_ANALYSIS.md)

---

## 11. Conclusion

The Smart City Environmental Monitoring platform demonstrates a production-style distributed architecture: event-driven ingestion, stream processing, durable storage, API aggregation, and a live dashboard. The repository includes runnable code, infrastructure scripts, CI/CD automation, diagrams, and operational screenshots suitable for capstone evaluation.
