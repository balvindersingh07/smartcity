# Smart City Environmental Monitoring

[![CI](https://github.com/balvindersingh07/smartcity/actions/workflows/ci-cd.yml/badge.svg?branch=main)](https://github.com/balvindersingh07/smartcity/actions/workflows/ci-cd.yml)

**Live repo:** [github.com/balvindersingh07/smartcity](https://github.com/balvindersingh07/smartcity)

Production-style **distributed system** for real-time environmental sensor data: **microservices** (Python / FastAPI), **Kafka** streaming, **PostgreSQL**, **React** dashboard, **Docker**, **Kubernetes (AKS)** on **Azure**, with **GitHub Actions** CI/CD and images on **GHCR**.

This file is the **GitHub repository home page** (root `README.md`). Application code lives under [`smart-city/`](smart-city/).

---

## Repository on GitHub

![GitHub repository overview](docs/images/screenshot-github-repo-home.png)

---

## Project banner

![Smart City banner](docs/images/banner.svg)

---

## Tech stack

| Layer | Technologies |
|------|----------------|
| Microservices | Python, FastAPI |
| Frontend | React, Vite |
| Messaging | Apache Kafka (Redpanda in cluster) |
| Data | PostgreSQL |
| Cloud | Azure (AKS, Container Registry, budgets, Application Insights) |
| IaC | Terraform (HCL) |
| CI/CD | GitHub Actions, GHCR |

---

## Architecture (diagrams)

### Microservices

![Microservices architecture](docs/images/architecture-microservices.svg)

### Data flow

![Data flow](docs/images/data-flow.svg)

### CI/CD and Azure

![CI/CD and Azure](docs/images/cicd-azure.svg)

---

## Screenshots

### Environmental monitoring dashboard (UI)

![Environmental monitoring dashboard](docs/images/screenshot-ui-dashboard.png)

### CI/CD: successful pipeline (staging then production)

Tests, Docker build, push to GHCR, deploy to AKS staging, then production.

![Successful GitHub Actions CI/CD run](docs/images/screenshot-github-cicd-success-run.png)

### Azure: staging resources (AKS, ACR, networking)

![Azure all resources staging](docs/images/screenshot-azure-all-resources-staging.png)

### Azure: Application Insights (monitoring)

![Application Insights staging](docs/images/screenshot-azure-application-insights-staging.png)

### Azure: monthly budget (cost control)

![Azure monthly budget](docs/images/screenshot-azure-monthly-budget.png)

### GitHub Actions: workflow run history

![GitHub Actions run history](docs/images/screenshot-github-actions-run-history.png)

<details>
<summary><b>CI/CD troubleshooting (historical)</b> - click to expand failure screenshots</summary>

![Single failed run](docs/images/screenshot-github-actions-single-failed-run.png)

![Workflow graph failed](docs/images/screenshot-github-actions-workflow-graph-failed.png)

![Frontend Vite permission error](docs/images/screenshot-github-frontend-vite-permission-denied.png)

![Processing service test failure](docs/images/screenshot-github-processing-service-test-failure.png)

![Publish images processing failed](docs/images/screenshot-github-publish-images-processing-failed.png)

![Azure login deploy staging](docs/images/screenshot-github-azure-login-deploy-staging.png)

</details>

---

## Features

- **Services:** ingestion, processing, storage, API, notification (FastAPI)
- **Streaming:** Kafka topics for sensor events and downstream processing
- **Storage:** PostgreSQL (metadata and sensor time-series data)
- **Frontend:** React dashboard (`smart-city/frontend-react`)
- **Kubernetes:** manifests under `smart-city/kubernetes/` (deps, network policies, HPA, ingress)
- **CI/CD:** on push to `main`, build and push `ghcr.io/<owner>/smart-city-<service>:<sha>`, deploy to staging then production AKS

---

## Repository layout

```text
.
??? .github/workflows/ci-cd.yml
??? docs/images/                 # Diagrams (SVG) and screenshots (PNG) for this README
??? README.md                    # This file (GitHub home page)
??? DESIGN_SYSTEM.md
??? app.js, index.html, styles.css
??? smart-city/
?   ??? README.md                # Quick start inside the app folder
?   ??? docker-compose.yml
?   ??? services/                # microservices
?   ??? frontend-react/
?   ??? kubernetes/
?   ??? terraform/
?   ??? kafka/
?   ??? ci-cd/
??? submission/                  # Capstone DOCX generator (optional)
```

Folder-only quick reference: **[smart-city/README.md](smart-city/README.md)**

---

## Quick start (local)

```bash
cd smart-city
docker compose up --build
```

| Service | Swagger |
|---------|---------|
| Ingestion | http://localhost:8001/docs |
| Processing | http://localhost:8002/docs |
| Storage | http://localhost:8003/docs |
| API | http://localhost:8004/docs |
| Notification | http://localhost:8005/docs |

Frontend dev:

```bash
cd smart-city/frontend-react
npm install
npm run dev
```

Example ingest:

```bash
curl -X POST http://localhost:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":"sensor-001","type":"temperature","value":31.5,"timestamp":"2026-04-15T10:00:00Z","location_id":"zone-a"}'
```

---

## Kubernetes (AKS) and CI/CD

Workflow: **[`.github/workflows/ci-cd.yml`](.github/workflows/ci-cd.yml)**

- Pushes to `main` run tests, build images, publish to GHCR, then `kubectl apply` and `kubectl set image` for staging and production.
- Manifests: `smart-city/kubernetes/`

**GitHub secrets (typical):**

| Secret | Purpose |
|--------|---------|
| `AZURE_CREDENTIALS` | Service principal JSON for `azure/login` |
| `AKS_RG_STAGING` | Staging resource group |
| `AKS_CLUSTER_STAGING` | Staging cluster name |
| `AKS_RG_PROD` | Production resource group |
| `AKS_CLUSTER_PROD` | Production cluster name |

Use GitHub **Environments** `staging` and `production` for approvals and secrets.

More: [smart-city/kubernetes/README.md](smart-city/kubernetes/README.md), [smart-city/ci-cd/README.md](smart-city/ci-cd/README.md)

---

## Terraform (Azure)

```bash
cd smart-city/terraform
terraform init
terraform plan -var-file=prod.tfvars -out tfplan
terraform apply tfplan
```

See [smart-city/terraform/README.md](smart-city/terraform/README.md).

---

## Security and monitoring

- Health and Prometheus-style metrics on services where implemented
- Kubernetes RBAC and NetworkPolicies
- Optional Log Analytics / Application Insights via Terraform

---

## Capstone report (DOCX)

```bash
pip install python-docx
python submission/generate_capstone_report_docx.py
```

Output: `submission/Smart_City_Environmental_Monitoring_Capstone_Report.docx`

---

## License

Specify your license (e.g. MIT) here if the repository is public.
