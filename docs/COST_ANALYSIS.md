# Cost Analysis Report

## Overview

Cloud costs are controlled through **right-sized AKS nodes**, **managed PostgreSQL tier selection**, and **Azure subscription budget alerts** defined in Terraform.

Screenshot evidence: `docs/images/screenshot-azure-monthly-budget.png`

---

## Provisioned resources (staging / production pattern)

| Resource | Purpose | Cost driver |
|----------|---------|-------------|
| AKS cluster | Microservices orchestration | Node VM size × count |
| PostgreSQL Flexible Server | Sensor metadata + time-series | SKU (vCores, storage GB) |
| Virtual Network | Private networking | Minimal |
| Application Insights | Telemetry | Ingested data volume |
| Container registry (GHCR) | Docker images | Storage + transfer |
| Vercel (frontend) | Dashboard hosting | Free tier for capstone demo |

Terraform: `smart-city/terraform/`

---

## Estimated monthly cost (indicative)

Use [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/) for your region. Example staging profile:

| Component | Example SKU | Est. USD/month |
|-----------|-------------|----------------|
| AKS (2 nodes) | Standard_D2s_v3 | ~$140–180 |
| PostgreSQL | Burstable B1ms | ~$25–40 |
| Log Analytics | Pay-as-you-go (low volume) | ~$5–20 |
| Egress / LB | Variable | ~$10–30 |
| **Total (staging)** | | **~$180–270** |

Production would scale node pool and database tier; use separate resource groups (`AKS_RG_STAGING` vs `AKS_RG_PROD` in CI/CD).

---

## Cost governance

### Budget alerts (Terraform)

When `enable_budget_alert=true` and `subscription_id` is set:

- Subscription-scope monthly budget  
- Email notification at threshold (e.g. 80% forecast)

Variable: `budget_contact_emails` in `smart-city/terraform/variables.tf`

### Operational practices

- Scale-to-zero not used (services need uptime for demo); HPA caps max replicas  
- Staging cluster can be stopped/deallocated when not evaluating  
- GHCR instead of ACR reduces duplicate registry cost for student projects  

---

## Cost vs capstone requirements

| Requirement | Implementation |
|-------------|----------------|
| Azure Cost Management | Budget resource in Terraform |
| Budget alerts | Email on forecast threshold |
| Track expenses | Azure portal Cost Analysis + screenshot in repo |

---

## Recommendation for evaluators

Review `screenshot-azure-monthly-budget.png` and Terraform budget block in `smart-city/terraform/main.tf` for automated cost governance evidence.
