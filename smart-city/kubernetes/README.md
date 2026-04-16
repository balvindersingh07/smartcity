# Kubernetes Manifests (AKS-Ready Baseline)

Apply in order:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.example.yaml
kubectl apply -f rbac.yaml
kubectl apply -f dependencies.yaml
kubectl apply -f network-policies.yaml
kubectl apply -f ingestion.yaml
kubectl apply -f processing.yaml
kubectl apply -f storage.yaml
kubectl apply -f notification.yaml
kubectl apply -f api.yaml
kubectl apply -f hpa.yaml
kubectl apply -f pdb.yaml
kubectl apply -f ingress.yaml
```

Notes:

- `dependencies.yaml` ships in-cluster Postgres + Redpanda (Kafka protocol) for staging or demos. Swap for managed Azure Database / Event Hubs in production.
- Replace image names with your registry tags.
- Replace `secret.example.yaml` with real secrets (Key Vault CSI recommended on AKS). CI applies the example only in the **staging** job; production expects `smart-city-secrets` to exist already.
- Ensure your cluster has an ingress controller (NGINX/App Gateway Ingress).
