# Security & Monitoring

## Security

### Secrets management

| Layer | Mechanism | Location |
|-------|-----------|----------|
| Azure | Key Vault (optional) | `smart-city/terraform/main.tf` |
| Kubernetes | Secrets | `smart-city/kubernetes/secret.example.yaml` |
| CI/CD | GitHub Encrypted Secrets | `AZURE_CREDENTIALS`, AKS cluster names |

Production should use **Azure Key Vault CSI driver** on AKS instead of plain secret YAML.

### Kubernetes RBAC

`smart-city/kubernetes/rbac.yaml` defines service accounts and role bindings per workload — least-privilege access for ingestion, processing, storage, API, and notification pods.

### Network policies

`smart-city/kubernetes/network-policies.yaml` restricts ingress/egress:

- API service reachable on port 8004  
- Kafka broker ports limited to producer/consumer pods  
- Postgres accessible only from storage-service  

### Application security

- Input validation on ingest (Pydantic models, JSON schema)  
- CORS on API service for dashboard origins  
- No secrets in repository (`.gitignore` for `.env`, `*.tfvars`, terraform state)

---

## Monitoring

### Azure Monitor / Application Insights

Provisioned via Terraform when `enable_monitoring=true`:

- Log Analytics workspace  
- Application Insights linked to AKS  

Screenshot: `docs/images/screenshot-azure-application-insights-staging.png`

### Service-level metrics

Each microservice exposes:

- `GET /health` — liveness  
- `GET /metrics/prometheus` — Prometheus counters/histograms  

Examples: `ingest_requests_total`, `stored_events_total`, `api_request_latency_seconds`

### Alerting

- **Application-level:** processing-service publishes to `sensor-alerts` → notification-service  
- **Infrastructure-level:** Azure budget alerts, AKS pod restarts (via Azure Monitor)

---

## Operational dashboards

| View | Source |
|------|--------|
| Smart City dashboard | https://smartcity-mocha.vercel.app/ |
| API Swagger | http://98.70.234.97:8004/docs |
| GitHub Actions CI | https://github.com/balvindersingh07/smartcity/actions |
| Azure portal | Staging resource group screenshot in `docs/images/` |

---

## Capstone rubric mapping

| Criteria | Evidence |
|----------|----------|
| Secret management | Key Vault (Terraform), K8s secrets, GitHub secrets |
| Access controls | RBAC, NetworkPolicies |
| Service health monitoring | /health, Application Insights |
| Failure alerts | sensor-alerts pipeline, Azure budget alerts |
