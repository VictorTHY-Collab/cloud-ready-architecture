# AI-Ready Platform Guide

This guide extends the production cloud architecture into an AI-ready enterprise platform.

## Base platform

```text
AWS VPC
  -> EKS
  -> RDS / databases
  -> observability
  -> CI/CD
```

## AI-ready platform layer

Add:

```text
AI workflow layer
  -> LangGraph / n8n / internal agents
  -> MCP tools
  -> database automation tools
  -> incident response playbooks
  -> self-healing workflows
```

## Suggested components

| Area | Recommended tool |
|---|---|
| Agent orchestration | LangGraph |
| Workflow automation | n8n |
| Developer AI | Codex, Claude Code, Cursor |
| Infra automation | Terraform/OpenTofu |
| Runtime | Kubernetes/EKS |
| Observability | OpenTelemetry, Prometheus, Grafana |
| Policy | OPA Gatekeeper or Kyverno |
| Secrets | AWS Secrets Manager / External Secrets Operator |

## AI database operations use cases

- database health check agent
- slow SQL triage agent
- replication lag investigation
- backup validation workflow
- capacity forecast workflow
- incident summary generator
- deployment risk review agent
- patch readiness checklist generator

## Self-healing example

```text
Alert: database connection spike
  -> collect metrics
  -> check app deployment timeline
  -> inspect DB sessions
  -> compare baseline
  -> create incident summary
  -> recommend action
  -> optionally trigger approved remediation
```

## Governance guardrails

AI automation should not directly change production without:

- approval workflow
- audit log
- rollback plan
- limited IAM permission
- change ticket reference
- human confirmation for destructive actions

## Leadership positioning

This architecture can be presented as:

> AI-ready cloud platform foundation for secure, observable, self-healing enterprise workloads.
