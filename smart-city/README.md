# Smart City application (`smart-city/`)

This directory contains **Docker Compose**, **microservices**, **Kubernetes manifests**, **Terraform**, **Kafka** config, and the **React** frontend.

**Full documentation, diagrams, and all screenshots** (GitHub repo home page): **[`README.md` in the repository root](../README.md)**.

---

## Quick start (run from this folder)

```bash
docker compose up --build
```

| Service | Local URL |
|---------|-----------|
| Ingestion | http://localhost:8001/docs |
| Processing | http://localhost:8002/docs |
| Storage | http://localhost:8003/docs |
| API | http://localhost:8004/docs |
| Notification | http://localhost:8005/docs |

**Frontend:**

```bash
cd frontend-react && npm install && npm run dev
```

**Database migrations (storage):**

```bash
cd services/storage-service && alembic upgrade head
```

---

## Layout

```text
services/          # ingestion, processing, storage, api, notification
kubernetes/        # AKS YAML
terraform/         # Azure IaC
frontend-react/
kafka/
ci-cd/
```

More: [kubernetes/README.md](kubernetes/README.md) | [terraform/README.md](terraform/README.md)
