# Production Cloud Ready Architecture Starter

This repository is a production-oriented starter blueprint for a cloud-native platform using:

- AWS landing-zone style network segmentation
- Terraform/OpenTofu infrastructure as code
- Amazon EKS for container workloads
- Amazon RDS PostgreSQL for managed database
- Private subnets for application and data tiers
- NAT egress, controlled ingress, security groups
- KMS encryption, CloudWatch logging, SNS alert channel
- Kubernetes manifests using Kustomize overlays
- GitHub Actions CI/CD example

> Default cloud: AWS. The structure is intentionally modular so you can adapt it to Azure, GCP, OCI, or hybrid enterprise platforms later.

---

## 1. Architecture Overview

```text
Users / API Clients
        |
        v
DNS / WAF / ALB
        |
        v
Amazon EKS private worker nodes
        |
        +--> Application pods
        +--> Service accounts with IAM roles
        +--> Observability agents
        |
        v
Amazon RDS PostgreSQL private data subnets

Supporting services:
- VPC across multiple availability zones
- Public, private, and database subnets
- NAT gateways for outbound private subnet access
- KMS encryption
- CloudWatch logs and alarms
- SNS notification topic
- GitHub Actions pipeline
```

---

## 2. Repository Structure

```text
.
├── architecture/
│   └── architecture.md
├── app/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── cicd/
│   └── github-actions/
│       └── deploy.yml
├── docs/
│   ├── AI_READY_PLATFORM_GUIDE.md
│   ├── CI_CD_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── GITHUB_UPLOAD_GUIDE.md
│   ├── KUBERNETES_GUIDE.md
│   ├── TERRAFORM_GUIDE.md
│   ├── decisions.md
│   ├── runbook.md
│   └── security-checklist.md
├── k8s/
│   ├── base/
│   └── overlays/
│       ├── dev/
│       └── prod/
├── scripts/
├── terraform/
│   ├── envs/
│   │   ├── dev/
│   │   └── prod/
│   └── modules/
│       ├── eks/
│       ├── kms/
│       ├── network/
│       ├── observability/
│       ├── rds/
│       └── security/
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 3. Quick Start

### Prerequisites

Install:

- Terraform or OpenTofu
- AWS CLI
- kubectl
- Docker
- GitHub CLI, optional

Authenticate to AWS:

```bash
aws configure
```

Or use SSO:

```bash
aws sso login --profile your-profile
export AWS_PROFILE=your-profile
```

---

## 4. Deploy Infrastructure

### Dev environment

```bash
cd terraform/envs/dev
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

### Prod environment

```bash
cd terraform/envs/prod
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

---

## 5. Configure Kubernetes Access

After EKS is provisioned:

```bash
aws eks update-kubeconfig \
  --region ap-southeast-1 \
  --name dev-cloud-ready-eks
```

Validate:

```bash
kubectl get nodes
kubectl get ns
```

---

## 6. Deploy Application

Dev:

```bash
kubectl apply -k k8s/overlays/dev
```

Prod:

```bash
kubectl apply -k k8s/overlays/prod
```

Check rollout:

```bash
kubectl rollout status deployment/cloud-ready-app -n cloud-ready-dev
kubectl get pods -A
```

---

## 7. CI/CD

The GitHub Actions workflow is available at:

```text
.github/workflows/deploy.yml
```

A copy is also stored under:

```text
cicd/github-actions/deploy.yml
```

Recommended GitHub secrets:

```text
AWS_ROLE_TO_ASSUME
AWS_REGION
ECR_REPOSITORY
EKS_CLUSTER_NAME
```

---

## 8. Production Hardening Checklist

Before using this directly for production, review:

- Remote Terraform state in S3 with DynamoDB locking
- Least-privilege IAM roles
- Private-only database access
- RDS backup retention and deletion protection
- EKS logging and audit logs
- Network policies
- Pod security standards
- Secrets management through AWS Secrets Manager or External Secrets Operator
- Image scanning
- CI/CD approval gates
- Observability and alert routing

See:

```text
docs/security-checklist.md
docs/runbook.md
docs/DEPLOYMENT_GUIDE.md
```

---

## 9. Suggested Next Evolution

To make this more enterprise and AI-platform ready, add:

- Argo CD for GitOps
- External Secrets Operator
- AWS Load Balancer Controller
- Karpenter for autoscaling
- Prometheus, Grafana, Loki, Tempo
- OpenTelemetry collector
- Kyverno or OPA Gatekeeper
- HashiCorp Vault or AWS Secrets Manager
- Self-healing automation agents
- Database automation workflows
- LangGraph/n8n platform automation layer

See:

```text
docs/AI_READY_PLATFORM_GUIDE.md
```

---

## 10. Important Notes

This repository is a starter architecture. Before production use, align it with your organization standards for:

- Account structure
- Network CIDR ranges
- Security policy
- Compliance controls
- Backup policy
- Disaster recovery RTO/RPO
- Logging retention
- Cost management
- Tagging standards

