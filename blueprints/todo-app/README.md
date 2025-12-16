# Todo App Blueprint

## Overview
Complete deployment blueprint for the Evolution of Todo application.

## Prerequisites
- Kubernetes cluster (Minikube, AKS, GKE, EKS)
- kubectl configured
- Helm 3+
- Dapr CLI installed

## Quick Start

```bash
# Set environment variables
export DATABASE_URL="postgresql+asyncpg://user:pass@host/db"
export BETTER_AUTH_SECRET="your-secret"
export OPENAI_API_KEY="sk-your-key"

# Deploy
./deploy.sh --domain todo.example.com

# Dry run first
./deploy.sh --domain todo.local --dry-run
```

## Configuration Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--cluster-name` | Cluster to deploy to | Current context |
| `--database-url` | PostgreSQL connection string | Required |
| `--domain` | Application domain | todo.local |
| `--dry-run` | Preview without deploying | false |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Neon PostgreSQL connection |
| `BETTER_AUTH_SECRET` | Yes | JWT signing secret |
| `OPENAI_API_KEY` | Yes | OpenAI API key for chat |
| `NAMESPACE` | No | Kubernetes namespace (default) |
| `RELEASE_NAME` | No | Helm release name (todo-app) |

## What Gets Deployed

1. **Backend Deployment**
   - FastAPI container
   - Dapr sidecar
   - Health checks
   - Resource limits

2. **Frontend Deployment**
   - Next.js container
   - Health checks
   - Resource limits

3. **Services**
   - Backend ClusterIP
   - Frontend ClusterIP

4. **Ingress**
   - Path-based routing
   - / → Frontend
   - /api → Backend

5. **Secrets**
   - DATABASE_URL
   - BETTER_AUTH_SECRET
   - OPENAI_API_KEY

6. **Dapr Components**
   - kafka-pubsub (Redpanda)
   - statestore (PostgreSQL)
   - reminder-cron (5 min)
   - kubernetes-secrets

## Verification

```bash
# Check pods
kubectl get pods

# Check services
kubectl get svc

# View backend logs
kubectl logs -f deployment/todo-backend

# Port forward for testing
kubectl port-forward svc/todo-backend 8000:8000
```

## Cleanup

```bash
# Remove deployment
helm uninstall todo-app

# Remove Dapr components
kubectl delete -f ../../dapr/components/

# Remove namespace (if dedicated)
kubectl delete namespace todo-app
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
```

### Database connection failed
- Verify DATABASE_URL is correct
- Check network policies
- Verify Neon DB IP allowlist

### Ingress not working
```bash
# Verify ingress controller
kubectl get pods -n ingress-nginx

# Check ingress
kubectl describe ingress todo-ingress
```
