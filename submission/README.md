# Capstone Final Submission — Smart City Environmental Monitoring

**Candidate repository:** [github.com/balvindersingh07/smartcity](https://github.com/balvindersingh07/smartcity)

This folder is the **submission index**. Evaluators can find all deliverables from this repo without extra zip files.

---

## Live demos

| Item | URL |
|------|-----|
| **Live frontend (Vercel)** | https://smartcity-mocha.vercel.app/ |
| **API docs (staging)** | http://98.70.234.97:8004/docs |
| **CI/CD pipeline** | https://github.com/balvindersingh07/smartcity/actions |

---

## Project report (Markdown — copy to Word/PDF for portal)

| Section | Document |
|---------|----------|
| Full report (requirements, architecture, summary) | [docs/PROJECT_REPORT.md](../docs/PROJECT_REPORT.md) |
| Database design | [docs/DATABASE_DESIGN.md](../docs/DATABASE_DESIGN.md) |
| Stream processing | [docs/STREAM_PROCESSING.md](../docs/STREAM_PROCESSING.md) |
| Security & monitoring | [docs/SECURITY_AND_MONITORING.md](../docs/SECURITY_AND_MONITORING.md) |
| Cost analysis | [docs/COST_ANALYSIS.md](../docs/COST_ANALYSIS.md) |
| Video walkthrough script (10–15 min) | [docs/VIDEO_WALKTHROUGH.md](../docs/VIDEO_WALKTHROUGH.md) |

**Diagrams (PNG — insert into Word/PDF):** [`docs/images/`](../docs/images/)

| Diagram | File |
|---------|------|
| Microservices architecture | `architecture-microservices.png` |
| Data flow | `data-flow.png` |
| CI/CD & Azure cloud | `cicd-azure.png` |
| Dashboard UI | `screenshot-ui-dashboard.png` |
| Azure resources (staging) | `screenshot-azure-all-resources-staging.png` |
| Application Insights | `screenshot-azure-application-insights-staging.png` |
| Cost budget alert | `screenshot-azure-monthly-budget.png` |
| CI/CD success run | `screenshot-github-cicd-success-run.png` |

---

## Code repository deliverables

| Deliverable | Location |
|-------------|----------|
| Microservices + Dockerfiles | [`smart-city/services/`](../smart-city/services/) |
| Docker Compose (local) | [`smart-city/docker-compose.yml`](../smart-city/docker-compose.yml) |
| Kafka topics & message schema | [`smart-city/kafka/`](../smart-city/kafka/) |
| Frontend dashboard | [`smart-city/frontend-react/`](../smart-city/frontend-react/) |
| Kubernetes manifests (AKS) | [`smart-city/kubernetes/`](../smart-city/kubernetes/) |
| Terraform (Azure IaC) | [`smart-city/terraform/`](../smart-city/terraform/) |
| CI/CD workflow | [`.github/workflows/ci-cd.yml`](../.github/workflows/ci-cd.yml) |
| Setup & run instructions | [README.md](../README.md) |

---

## Quick local verification

```bash
cd smart-city
docker compose up -d --build
```

```bash
curl -X POST http://localhost:8001/ingest \
  -H "Content-Type: application/json" \
  -d '{"sensor_id":"demo-001","type":"temperature","value":29.5,"timestamp":"2026-05-27T12:00:00Z"}'
```

```bash
cd smart-city/frontend-react && npm install && npm run dev
```

Open http://localhost:5173 — dashboard reads API at http://localhost:8004.

---

## Capstone rubric mapping

| Rubric area | Evidence in this repo |
|-------------|------------------------|
| Architecture design | Diagrams + [PROJECT_REPORT.md](../docs/PROJECT_REPORT.md) |
| Messaging & streaming | Kafka + [STREAM_PROCESSING.md](../docs/STREAM_PROCESSING.md) |
| Database design | PostgreSQL + [DATABASE_DESIGN.md](../docs/DATABASE_DESIGN.md) |
| Containerization & K8s | Dockerfiles, Compose, `smart-city/kubernetes/` |
| CI/CD | GitHub Actions + screenshots |
| Security | RBAC, NetworkPolicies, Key Vault (Terraform) |
| Monitoring & cost | Application Insights, budget alerts, Prometheus metrics |
