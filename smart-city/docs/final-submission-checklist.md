# Final Submission Checklist

Use this checklist to close all rubric items before submission.

## 1. Architecture & Design

- [ ] Functional requirements documented
- [ ] Non-functional requirements documented
- [ ] Microservice architecture diagram included
- [ ] Data flow diagram included
- [ ] Azure infrastructure diagram included

## 2. Messaging & Streaming

- [ ] Kafka topics documented (`raw`, `processed`, `alerts`, `dlq`)
- [ ] Event contract documented
- [ ] Stream filtering + aggregation evidence captured
- [ ] Anomaly alert flow demonstrated

## 3. Database

- [ ] ER design for `locations`, `sensors`, `sensor_data`
- [ ] Migration strategy documented (Alembic)
- [ ] Write/query optimization notes included

## 4. Deployment

- [ ] Dockerfiles for all services
- [ ] Docker Compose runbook included
- [ ] Kubernetes manifests validated in cluster
- [ ] HPA and PDB applied

## 5. CI/CD

- [ ] Build/test/image publish flow passing
- [ ] Staging deployment with smoke test
- [ ] Production deployment with approval gate

## 6. Security

- [ ] Secrets externalized (env/Key Vault)
- [ ] RBAC manifests applied
- [ ] Network policies applied
- [ ] Containers run as non-root

## 7. Monitoring & Cost

- [ ] Prometheus endpoints validated
- [ ] App Insights/Log Analytics configured (if Azure-enabled)
- [ ] Alert action group configured
- [ ] Cost budget configured and tested

## 8. Demo Assets

- [ ] README setup is reproducible
- [ ] 10–15 minute walkthrough video recorded
- [ ] Final report exported to PDF
