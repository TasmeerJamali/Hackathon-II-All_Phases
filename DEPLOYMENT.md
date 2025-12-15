# Kubernetes Deployment Guide

## Prerequisites

- Docker Desktop or Minikube
- kubectl CLI
- Helm 3+

## Option 1: Minikube Deployment

### 1. Start Minikube
```bash
minikube start --cpus=2 --memory=4096
```

### 2. Point Docker to Minikube
```bash
eval $(minikube docker-env)
```

### 3. Build Docker Images
```bash
# Build backend
docker build -t todo-backend:latest ./backend

# Build frontend  
docker build -t todo-frontend:latest ./frontend
```

### 4. Create Secrets File
Create `helm/todo-evolution/values-local.yaml`:
```yaml
secrets:
  databaseUrl: "postgresql+asyncpg://user:pass@host/db"
  betterAuthSecret: "your-secret-key"
  openaiApiKey: "sk-your-openai-key"
```

### 5. Deploy with Helm
```bash
helm install todo-app ./helm/todo-evolution -f helm/todo-evolution/values-local.yaml
```

### 6. Enable Ingress
```bash
minikube addons enable ingress
```

### 7. Access Application
```bash
# Add to /etc/hosts: 127.0.0.1 todo.local
minikube tunnel
```

Open http://todo.local in browser.

---

## Option 2: Docker Compose (Local Dev)

```bash
# Create .env file with secrets
cp backend/.env.example .env

# Start services
docker-compose up --build
```

---

## kubectl Commands

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# View logs
kubectl logs -f deployment/todo-backend

# Port forward (alternative to ingress)
kubectl port-forward service/todo-backend 8000:8000
kubectl port-forward service/todo-frontend 3000:3000
```
