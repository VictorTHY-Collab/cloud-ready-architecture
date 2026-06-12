# Security Checklist

## Cloud account

- Use separate accounts for dev, staging, and prod.
- Enable MFA for human users.
- Avoid long-lived access keys.
- Use IAM Identity Center or SSO.
- Enable CloudTrail.

## Network

- Keep application nodes in private subnets.
- Keep databases in isolated data subnets.
- Restrict inbound access by security group.
- Avoid public database endpoints.
- Use VPC endpoints for private AWS service access where possible.

## Kubernetes

- Enable EKS audit logging.
- Use least-privilege service accounts.
- Enforce pod security standards.
- Apply network policies.
- Set resource requests and limits.
- Use image scanning.

## Secrets

- Do not commit secrets.
- Use AWS Secrets Manager, SSM Parameter Store, or External Secrets Operator.
- Rotate credentials.
- Use GitHub OIDC to AWS instead of static cloud keys.

## Database

- Enable encryption at rest.
- Enable backup retention.
- Test restore procedures.
- Restrict database security groups.
- Use deletion protection for production.
- Use parameter groups and audit logging where required.

## CI/CD

- Separate plan and apply.
- Require manual approval for production.
- Run IaC scanning.
- Run container image scanning.
- Protect main branch.
- Require pull request reviews.

## AI automation guardrails

- Give agents read-only access by default.
- Require approval for production changes.
- Log every AI-generated action.
- Keep rollback instructions close to every automated remediation.
