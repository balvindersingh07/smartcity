# Cost Governance Guide

## Cost Controls Implemented

- Terraform support for `azurerm_consumption_budget_subscription`
- Budget threshold notification at 80%
- Configurable monthly cap via `monthly_budget_amount`

## Suggested Budget Baseline (Dev)

- AKS node pool: 45–60%
- PostgreSQL Flexible Server: 20–30%
- Monitoring/Logs: 10–15%
- Registry + networking + misc: 10%

## Actions to Enable

1. Set `subscription_id` in terraform variables.
2. Set `enable_budget_alert=true`.
3. Provide `budget_contact_emails`.
4. Apply terraform.

## FinOps Practices

- Use lower-cost SKU for non-prod.
- Scale node pools by schedules.
- Set log retention to practical limits.
- Track unit cost per 1K ingested events.
