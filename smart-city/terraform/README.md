# Terraform (Simplified)

## What It Provisions

- Resource Group
- Virtual Network + AKS subnet
- AKS cluster
- PostgreSQL Flexible Server + database
- Key Vault (optional)
- Log Analytics + Application Insights (optional)
- Subscription budget alert (optional)

## Usage

```bash
terraform init
terraform plan -out tfplan
terraform apply tfplan
```

### Optional Variables

- `enable_key_vault=true|false`
- `enable_monitoring=true|false`
- `enable_budget_alert=true|false`
- `subscription_id=<azure-subscription-id>` (required for budget resource)
- `budget_contact_emails=["ops@example.com"]`

Use this as a baseline and split into modules (`network`, `aks`, `database`, `security`, `monitoring`) for production.
