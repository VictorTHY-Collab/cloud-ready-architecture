# CI/CD Guide

## Target CI/CD pattern

```text
Developer push
  -> GitHub Actions
  -> Terraform validate / plan
  -> Docker build
  -> ECR push
  -> Kubernetes deploy or GitOps sync
```

## Generated workflow

Run:

```bash
python tools/generate_scaffold.py
```

This creates:

```text
.github/workflows/deploy.yml
```

## Recommended GitHub secrets

```text
AWS_DEPLOY_ROLE_ARN
AWS_REGION
ECR_REPOSITORY
EKS_CLUSTER_NAME
```

## Recommended permissions

Use GitHub OIDC instead of long-lived AWS keys.

```yaml
permissions:
  id-token: write
  contents: read
```

## Production deployment gate

Recommended flow:

```text
Pull request
  -> terraform fmt
  -> terraform validate
  -> security scan
  -> terraform plan
  -> manual approval
  -> terraform apply
  -> image build
  -> deploy through GitOps
```

## Security scans

Add:

- checkov
- tfsec
- trivy
- gitleaks
- kube-score
- conftest / OPA

## Best practice

For production, CI should build and publish artifacts. CD should be handled by GitOps, such as Argo CD, for better auditability and rollback.
