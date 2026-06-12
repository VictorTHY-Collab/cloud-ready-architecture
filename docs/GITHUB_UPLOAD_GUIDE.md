# GitHub Upload Guide

This repo has been initialized through the GitHub connector.

## Clone

```bash
git clone https://github.com/VictorTHY-Collab/cloud-ready-architecture.git
cd cloud-ready-architecture
```

## Generate full scaffold

```bash
python tools/generate_scaffold.py
```

## Commit generated files

```bash
git add .
git commit -m "feat: generate production cloud scaffold"
git push origin main
```

## Suggested branch protection

Enable:

- Require pull request before merging
- Require status checks
- Require conversation resolution
- Restrict force push
- Require signed commits if your organization uses it

## Suggested repository description

```text
Production cloud-ready AWS/EKS/Terraform/Kubernetes architecture scaffold with AI-ready platform extension guides.
```
