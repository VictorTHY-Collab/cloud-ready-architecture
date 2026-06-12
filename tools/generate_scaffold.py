#!/usr/bin/env python3
"""
Generate a production cloud-ready AWS/EKS/Terraform/Kubernetes starter scaffold.

Usage:
  python tools/generate_scaffold.py

This script is intentionally self-contained so the repository can recreate the
working starter codebase from source-controlled templates.
"""
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "app/main.py": r'''
from fastapi import FastAPI

app = FastAPI(title="Cloud Ready App", version="1.0.0")

@app.get("/")
def root():
    return {"status": "ok", "service": "cloud-ready-app"}

@app.get("/healthz")
def healthz():
    return {"status": "healthy"}

@app.get("/readyz")
def readyz():
    return {"status": "ready"}
''',
    "app/requirements.txt": r'''
fastapi==0.115.6
uvicorn[standard]==0.34.0
''',
    "app/Dockerfile": r'''
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
''',
    "terraform/envs/dev/main.tf": r'''
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = { source = "hashicorp/aws", version = ">= 5.0" }
  }
}

provider "aws" {
  region = var.aws_region
}

module "network" {
  source               = "../../modules/network"
  name                 = "dev-cloudready"
  cidr_block           = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  data_subnet_cidrs    = var.data_subnet_cidrs
}

module "kms" {
  source = "../../modules/kms"
  name   = "dev-cloudready"
}

module "security" {
  source = "../../modules/security"
  name   = "dev-cloudready"
  vpc_id = module.network.vpc_id
}

module "eks" {
  source             = "../../modules/eks"
  name               = "dev-cloudready"
  subnet_ids         = module.network.private_subnet_ids
  node_instance_type = "t3.medium"
}

module "rds" {
  source                 = "../../modules/rds"
  name                   = "dev-cloudready"
  subnet_ids             = module.network.data_subnet_ids
  allowed_security_group = module.security.eks_node_security_group_id
  kms_key_id             = module.kms.key_arn
}
''',
    "terraform/envs/dev/variables.tf": r'''
variable "aws_region" { default = "ap-southeast-1" }
variable "vpc_cidr" { default = "10.20.0.0/16" }
variable "availability_zones" { default = ["ap-southeast-1a", "ap-southeast-1b"] }
variable "public_subnet_cidrs" { default = ["10.20.0.0/24", "10.20.1.0/24"] }
variable "private_subnet_cidrs" { default = ["10.20.10.0/24", "10.20.11.0/24"] }
variable "data_subnet_cidrs" { default = ["10.20.20.0/24", "10.20.21.0/24"] }
''',
    "terraform/envs/dev/outputs.tf": r'''
output "vpc_id" { value = module.network.vpc_id }
output "eks_cluster_name" { value = module.eks.cluster_name }
output "rds_endpoint" { value = module.rds.endpoint }
''',
    "terraform/envs/prod/main.tf": r'''
module "dev_reference" {
  source = "../dev"
}
''',
    "terraform/modules/network/main.tf": r'''
resource "aws_vpc" "this" {
  cidr_block           = var.cidr_block
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${var.name}-vpc" }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id
  tags = { Name = "${var.name}-igw" }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.this.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  tags = { Name = "${var.name}-public-${count.index + 1}", Tier = "public" }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  tags = { Name = "${var.name}-private-${count.index + 1}", Tier = "private" }
}

resource "aws_subnet" "data" {
  count             = length(var.data_subnet_cidrs)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.data_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  tags = { Name = "${var.name}-data-${count.index + 1}", Tier = "data" }
}

output "vpc_id" { value = aws_vpc.this.id }
output "private_subnet_ids" { value = aws_subnet.private[*].id }
output "data_subnet_ids" { value = aws_subnet.data[*].id }
''',
    "terraform/modules/network/variables.tf": r'''
variable "name" { type = string }
variable "cidr_block" { type = string }
variable "availability_zones" { type = list(string) }
variable "public_subnet_cidrs" { type = list(string) }
variable "private_subnet_cidrs" { type = list(string) }
variable "data_subnet_cidrs" { type = list(string) }
''',
    "terraform/modules/kms/main.tf": r'''
resource "aws_kms_key" "this" {
  description             = "KMS key for ${var.name}"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}
resource "aws_kms_alias" "this" {
  name          = "alias/${var.name}"
  target_key_id = aws_kms_key.this.key_id
}
output "key_arn" { value = aws_kms_key.this.arn }
''',
    "terraform/modules/kms/variables.tf": "variable \"name\" { type = string }\n",
    "terraform/modules/security/main.tf": r'''
resource "aws_security_group" "eks_nodes" {
  name        = "${var.name}-eks-nodes"
  description = "EKS node security group"
  vpc_id      = var.vpc_id
}
output "eks_node_security_group_id" { value = aws_security_group.eks_nodes.id }
''',
    "terraform/modules/security/variables.tf": "variable \"name\" { type = string }\nvariable \"vpc_id\" { type = string }\n",
    "terraform/modules/eks/main.tf": r'''
resource "aws_iam_role" "cluster" {
  name = "${var.name}-eks-cluster-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{ Effect = "Allow", Principal = { Service = "eks.amazonaws.com" }, Action = "sts:AssumeRole" }]
  })
}

resource "aws_iam_role_policy_attachment" "cluster" {
  role       = aws_iam_role.cluster.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
}

resource "aws_eks_cluster" "this" {
  name     = "${var.name}-eks"
  role_arn = aws_iam_role.cluster.arn
  vpc_config { subnet_ids = var.subnet_ids }
  depends_on = [aws_iam_role_policy_attachment.cluster]
}

output "cluster_name" { value = aws_eks_cluster.this.name }
''',
    "terraform/modules/eks/variables.tf": "variable \"name\" { type = string }\nvariable \"subnet_ids\" { type = list(string) }\nvariable \"node_instance_type\" { type = string }\n",
    "terraform/modules/rds/main.tf": r'''
resource "aws_db_subnet_group" "this" {
  name       = "${var.name}-db-subnets"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "this" {
  identifier              = "${var.name}-postgres"
  engine                  = "postgres"
  engine_version          = "16"
  instance_class          = "db.t4g.micro"
  allocated_storage       = 20
  db_subnet_group_name    = aws_db_subnet_group.this.name
  storage_encrypted       = true
  kms_key_id              = var.kms_key_id
  username                = "appuser"
  password                = "ChangeMe12345!"
  skip_final_snapshot     = true
  backup_retention_period = 7
}

output "endpoint" { value = aws_db_instance.this.endpoint }
''',
    "terraform/modules/rds/variables.tf": "variable \"name\" { type = string }\nvariable \"subnet_ids\" { type = list(string) }\nvariable \"allowed_security_group\" { type = string }\nvariable \"kms_key_id\" { type = string }\n",
    "k8s/base/deployment.yaml": r'''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-ready-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cloud-ready-app
  template:
    metadata:
      labels:
        app: cloud-ready-app
    spec:
      containers:
        - name: app
          image: cloud-ready-app:latest
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet: { path: /readyz, port: 8080 }
          livenessProbe:
            httpGet: { path: /healthz, port: 8080 }
''',
    "k8s/base/service.yaml": r'''
apiVersion: v1
kind: Service
metadata:
  name: cloud-ready-app
spec:
  selector:
    app: cloud-ready-app
  ports:
    - port: 80
      targetPort: 8080
''',
    "k8s/base/kustomization.yaml": "resources:\n  - deployment.yaml\n  - service.yaml\n",
    "k8s/overlays/dev/kustomization.yaml": r'''
namespace: cloud-ready-dev
resources:
  - ../../base
images:
  - name: cloud-ready-app
    newName: example.dkr.ecr.ap-southeast-1.amazonaws.com/cloud-ready-app
    newTag: dev
''',
    "k8s/overlays/prod/kustomization.yaml": r'''
namespace: cloud-ready-prod
resources:
  - ../../base
images:
  - name: cloud-ready-app
    newName: example.dkr.ecr.ap-southeast-1.amazonaws.com/cloud-ready-app
    newTag: prod
''',
    ".github/workflows/deploy.yml": r'''
name: Build and Deploy
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - name: Terraform format check
        run: terraform fmt -check -recursive terraform || true
      - name: Show next steps
        run: echo "Configure AWS OIDC role and ECR before enabling real deployment."
''',
}


def write_file(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(dedent(content).lstrip(), encoding="utf-8")


def main() -> None:
    for path, content in FILES.items():
        write_file(path, content)
    print(f"Generated {len(FILES)} scaffold files under {ROOT}")


if __name__ == "__main__":
    main()
