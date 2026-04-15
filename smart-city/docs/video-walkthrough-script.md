# Video Walkthrough Script (10–15 minutes)

## 1) Intro (1 minute)

- Project goal: smart city real-time environmental monitoring
- Tech stack summary

## 2) Architecture (2 minutes)

- Explain service boundaries
- Show REST + Kafka communication flow
- Mention DLQ and anomaly path

## 3) Local Run Demo (3 minutes)

- Start compose stack
- Open service docs
- Push sample ingest events
- Show processing aggregates and alerts

## 4) Data Layer (2 minutes)

- Show PostgreSQL schema and migration setup
- Show metrics query output from storage/api service

## 5) Deployment & IaC (2 minutes)

- Walk through Kubernetes manifests (deployments, HPA, RBAC, network policies)
- Walk through Terraform resources (AKS, DB, Key Vault, monitoring)

## 6) CI/CD (2 minutes)

- Explain workflow stages:
  - test/build
  - image publish
  - staging deploy + smoke test
  - production gate

## 7) Security/Monitoring/Cost (2 minutes)

- Secret handling + RBAC + non-root containers
- Prometheus/App Insights hooks
- Budget alert setup

## 8) Closing (1 minute)

- Recap outcomes
- Mention future improvements (managed stream processing, ADX integration, SLO dashboards)
