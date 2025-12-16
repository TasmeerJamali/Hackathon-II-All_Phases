# Kubernetes Deployment Guide

> Phase IV: Local Kubernetes Deployment with AI-Powered Tools

## Prerequisites

- Docker Desktop 4.53+ (with Gordon AI) or Minikube
- kubectl CLI + kubectl-ai plugin
- Helm 3+
- kagent (optional)

---

## AI-Powered Kubernetes Tools

### kubectl-ai (AI-Powered kubectl)

```bash
# Install kubectl-ai
kubectl krew install ai
export OPENAI_API_KEY="your-key"

# Example commands for our project
kubectl ai "deploy backend with image todoevolutionacr.azurecr.io/backend:v1"
kubectl ai "scale backend deployment to 3 replicas"
kubectl ai "show logs from backend pod"
kubectl ai "why is my pod not starting"
kubectl ai "create a LoadBalancer service for backend on port 8000"
```

### kagent (Kubernetes AI Agent)

```bash
# Install kagent
pip install kagent

# Example commands
kagent analyze cluster          # Health check
kagent diagnose pod backend-xxx # Troubleshoot
kagent optimize deployment backend # Resource optimization
kagent security-scan            # Security audit
```

### Docker AI Gordon

Enable in Docker Desktop: Settings → Features in Development → Docker AI

```bash
docker ai "optimize my backend/Dockerfile"
docker ai "why is my container using so much memory"
docker ai "best practices for Python FastAPI containers"
```

📚 **Full documentation:** [docs/AI-K8S-TOOLS.md](docs/AI-K8S-TOOLS.md)

---

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
