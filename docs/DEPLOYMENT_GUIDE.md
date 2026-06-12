# Deployment Guide

This guide explains how to use this repository as a production cloud-ready starter architecture.

## 1. Generate the scaffold

```bash
python tools/generate_scaffold.py
```

This creates the Terraform, Kubernetes, application, and CI/CD scaffold folders.

## 2. Review architecture defaults

Default target platform:

```text
AWS + VPC + EKS + RDS PostgreSQL + CloudWatch + GitHub Actions
```

Default region:

```text
ap-southeast-1
```

Recommended production layout:

```text
public subnets   -> load balancer and NAT
private subnets  -> EKS worker nodes and app workloads
data subnets     -> RDS and private database services
```

## 3. Deploy infrastructure

```bash
cd terraform/envs/dev
terraform init
terraform validate
terraform plan
terraform apply
```

For production:

```bash
cd terraform/envs/prod
terraform init
terraform validate
terraform plan
terraform apply
```

## 4. Configure kubeconfig

```bash
aws eks update-kubeconfig \
  --region ap-southeast-1 \
  --name dev-cloudready-eks
```

## 5. Deploy app

```bash
kubectl apply -k k8s/overlays/dev
```

## 6. Production gates

Before production, add:

- Terraform remote state in S3
- DynamoDB lock table
- GitHub OIDC role for AWS deployment
- image scanning
- manual approval for production
- RDS deletion protection
- secrets manager integration
- monitoring and alerting
- backup and restore test

## 7. Important security note

The generated RDS module contains a demo password placeholder. Replace it with AWS Secrets Manager or a secure Terraform variable flow before any real deployment.
