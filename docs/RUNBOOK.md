# Operations Runbook

## Common commands

Generate scaffold:

```bash
python tools/generate_scaffold.py
```

Terraform validate:

```bash
cd terraform/envs/dev
terraform init
terraform validate
terraform plan
```

Kubernetes status:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
```

Application rollout:

```bash
kubectl rollout status deployment/cloud-ready-app -n cloud-ready-dev
kubectl logs -l app=cloud-ready-app -n cloud-ready-dev --tail=100
```

## Incident checklist

1. Confirm affected service and environment.
2. Check recent deployment or Terraform change.
3. Check Kubernetes pod status and events.
4. Check load balancer and ingress health.
5. Check database connectivity and RDS metrics.
6. Review logs and metrics.
7. Apply rollback or remediation.
8. Record post-incident action items.

## Rollback options

- rollback Kubernetes deployment
- revert Git commit
- restore previous image tag
- restore RDS snapshot if data issue
- roll back Terraform only after reviewing dependency impact

## Production notes

Keep remediation steps safe, reversible, and auditable. For AI-assisted operations, require human approval before destructive actions.
