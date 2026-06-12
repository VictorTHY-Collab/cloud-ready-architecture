# Kubernetes Guide

## Purpose

Kubernetes is used as the application runtime layer.

Generated structure:

```text
k8s/
  base/
    deployment.yaml
    service.yaml
    kustomization.yaml
  overlays/
    dev/
    prod/
```

## Generate manifests

```bash
python tools/generate_scaffold.py
```

## Deploy dev

```bash
kubectl apply -k k8s/overlays/dev
```

## Deploy prod

```bash
kubectl apply -k k8s/overlays/prod
```

## Validate rollout

```bash
kubectl get pods -A
kubectl get svc -A
kubectl rollout status deployment/cloud-ready-app -n cloud-ready-dev
```

## Production improvements

Add:

- namespace manifests
- resource requests and limits
- pod disruption budgets
- horizontal pod autoscaler
- network policies
- ingress controller
- external secrets
- service account IAM mapping
- pod security standards
- OpenTelemetry sidecar or collector

## Recommended GitOps evolution

Add Argo CD or Flux:

```text
GitHub repo -> Argo CD -> EKS cluster
```

This gives better production control than direct `kubectl apply` from a CI job.
