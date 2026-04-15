# CI/CD Notes

- Workflow file: `.github/workflows/ci-cd.yml`
- Pipeline stages:
  1. Install dependencies
  2. Run tests
  3. Build + push Docker images to GHCR
  4. Deploy to staging environment
  5. Smoke test
  6. Deploy to production environment (approval gate)

## Required GitHub Secrets

- `AZURE_CREDENTIALS`
- `AKS_RG_STAGING`
- `AKS_CLUSTER_STAGING`
- `AKS_RG_PROD`
- `AKS_CLUSTER_PROD`

## Environment Protection

Configure GitHub Environments `staging` and `production` with required reviewers for approval gates.
