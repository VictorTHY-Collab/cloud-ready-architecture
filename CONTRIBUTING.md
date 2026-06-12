# Contributing

## Recommended workflow

```bash
git checkout -b feature/your-change
python tools/generate_scaffold.py
terraform fmt -recursive terraform
terraform validate
git add .
git commit -m "feat: update cloud architecture scaffold"
git push
```

## Pull request checklist

- README updated if behavior changes
- Terraform formatted
- Kubernetes manifests validated
- No secrets committed
- Security checklist reviewed
- Production impact documented

## Commit examples

```text
feat: add eks scaffold generator
fix: improve rds production defaults
docs: add ai-ready platform guide
chore: update security checklist
```
