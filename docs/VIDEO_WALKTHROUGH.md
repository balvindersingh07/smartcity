# Video Walkthrough Script (10–15 minutes)

Record screen + voice. Upload link in college portal alongside GitHub repo.

---

## Links to show on screen

- Repo: https://github.com/balvindersingh07/smartcity  
- Live UI: https://smartcity-mocha.vercel.app/  
- CI/CD: https://github.com/balvindersingh07/smartcity/actions  
- Submission index: `submission/README.md`

---

## 0:00 – 2:00 | Architecture

1. Open GitHub README — scroll architecture diagrams  
2. Explain five microservices + Kafka + PostgreSQL  
3. Show `docs/images/architecture-microservices.png` and `data-flow.png`  

**Say:** "Sensor data enters ingestion, flows through Kafka, gets processed and stored, then API serves the dashboard."

---

## 2:00 – 5:00 | Local demo

1. Terminal: `cd smart-city && docker compose up -d`  
2. `docker compose ps` — all services Up  
3. Ingest sample event (PowerShell):

```powershell
Invoke-RestMethod -Uri "http://localhost:8001/ingest" -Method Post -ContentType "application/json" -Body '{"sensor_id":"demo-001","type":"temperature","value":29.5,"timestamp":"2026-05-27T12:00:00Z"}'
```

4. Open http://localhost:5173 (or `npm run dev` in frontend-react)  
5. Show metrics updating on dashboard  

---

## 5:00 – 8:00 | CI/CD & AKS

1. GitHub → Actions → successful workflow run  
2. Show stages: test → build → push GHCR → deploy staging → production  
3. Screenshot: `docs/images/screenshot-github-cicd-success-run.png`  
4. Briefly open `smart-city/kubernetes/` and `.github/workflows/ci-cd.yml`  

**Say:** "Every push to main triggers automated deployment to AKS with staging then production approval."

---

## 8:00 – 10:00 | Azure cloud & live frontend

1. Azure portal screenshot or live portal — AKS, resources  
2. Application Insights screenshot  
3. Open https://smartcity-mocha.vercel.app/ — "Production frontend on Vercel"  

---

## 10:00 – 12:00 | Security & monitoring

1. Show `smart-city/kubernetes/rbac.yaml` and `network-policies.yaml`  
2. Mention Key Vault in Terraform  
3. Show `/health` and Prometheus metrics endpoint in Swagger  

---

## 12:00 – 15:00 | Cost & wrap-up

1. Budget alert screenshot (`screenshot-azure-monthly-budget.png`)  
2. Recap submission folder: report docs, code, diagrams, live URLs  
3. Thank evaluator — repo has everything for review  

---

## Checklist before recording

- [ ] Docker running, compose stack up  
- [ ] Browser tabs pre-opened (GitHub, Vercel, Actions)  
- [ ] Microphone tested  
- [ ] Terminal font size readable  
