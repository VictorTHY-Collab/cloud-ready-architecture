# Production Cloud Architecture Guide

## Target outcome

A reusable production-ready cloud platform foundation that can host modern applications, APIs, automation workloads, and AI-ready services.

## Logical layers

```text
Users / API Clients
  -> DNS / CDN / WAF
  -> Application Load Balancer
  -> Kubernetes Ingress
  -> EKS application workloads
  -> RDS PostgreSQL / managed database services
  -> CloudWatch / logs / metrics / alerts
```

## Network design

Use a multi-AZ VPC with three subnet tiers:

| Tier | Purpose |
|---|---|
| Public | ALB, NAT gateway, internet-facing entry points |
| Private | EKS worker nodes, application pods, internal services |
| Data | RDS, cache, private data services |

## Compute design

EKS is used as the default compute platform because it provides:

- workload portability
- autoscaling options
- service isolation
- GitOps compatibility
- strong ecosystem support

## Database design

RDS PostgreSQL is used as the default database example. For enterprise use, extend the pattern for:

- Oracle on EC2 or RDS Custom
- SQL Server RDS / Always On on EC2
- MySQL / Aurora MySQL
- PostgreSQL / Aurora PostgreSQL
- MongoDB Atlas or DocumentDB

## Security design

Minimum production expectations:

- private app and data subnets
- least-privilege IAM
- KMS encryption
- audit logs
- image scanning
- no static cloud keys in CI/CD
- GitHub OIDC to AWS IAM role
- secret management through AWS Secrets Manager or External Secrets Operator

## Observability design

Recommended stack:

- CloudWatch for AWS-native logs and metrics
- Prometheus for Kubernetes metrics
- Grafana for dashboards
- Loki or OpenSearch for logs
- OpenTelemetry for traces
- SNS / PagerDuty / Slack for alerts

## Resilience design

Use:

- multiple availability zones
- horizontal pod autoscaling
- node autoscaling
- RDS backup retention
- tested restore procedure
- infrastructure drift detection
- runbooks for incident handling

## AI-ready extension

Add an automation layer for:

- self-healing runbooks
- infrastructure drift detection
- database health checks
- AI-assisted incident triage
- LangGraph or n8n workflow orchestration
- MCP tools for database and infrastructure operations
