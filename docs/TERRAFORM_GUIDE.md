# Terraform / OpenTofu Guide

## Purpose

Terraform is used to generate the cloud platform foundation.

Generated structure:

```text
terraform/
  envs/
    dev/
    prod/
  modules/
    network/
    security/
    kms/
    eks/
    rds/
```

## Recommended workflow

```bash
python tools/generate_scaffold.py
cd terraform/envs/dev
terraform init
terraform fmt -recursive
terraform validate
terraform plan
terraform apply
```

## Environment separation

Use one folder per environment:

```text
terraform/envs/dev
terraform/envs/prod
```

For real production, use separate AWS accounts or at least separate state files.

## Remote state recommendation

Use S3 backend and DynamoDB locking:

```hcl
terraform {
  backend "s3" {
    bucket         = "your-terraform-state-bucket"
    key            = "cloud-ready/dev/terraform.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

## Module design

Each module should have:

```text
main.tf
variables.tf
outputs.tf
README.md
```

## Production hardening

Add:

- input validation
- tagging standards
- encrypted state
- policy-as-code
- tfsec / checkov scan
- manual approval for production apply
- separate plan and apply workflow

## Important note

The scaffold is a starter. Review every CIDR, IAM policy, security group, backup setting, and database parameter before production use.
