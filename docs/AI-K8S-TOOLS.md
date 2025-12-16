# AI-Powered Kubernetes Tools Guide

> Phase IV: Using AI assistants for Kubernetes operations

---

## 1. kubectl-ai

kubectl-ai is an AI-powered kubectl plugin that generates Kubernetes commands from natural language.

### Installation

```bash
# Install via Krew (kubectl plugin manager)
kubectl krew install ai

# Or install directly with Go
go install github.com/sozercan/kubectl-ai@latest

# Set OpenAI API key
export OPENAI_API_KEY="sk-your-openai-key"
```

### Usage Examples

```bash
# Deploy our todo-backend
kubectl ai "deploy a pod running todoevolutionacr.azurecr.io/backend:v1 with 2 replicas"

# Scale deployment
kubectl ai "scale the backend deployment to 3 replicas"

# Check pod status
kubectl ai "show me all pods that are not running"

# Debug issues
kubectl ai "why is my backend pod crashing"

# Create a service
kubectl ai "expose backend deployment on port 8000 as a LoadBalancer"

# View logs
kubectl ai "show the last 50 lines of logs from the backend pod"

# Resource usage
kubectl ai "show me which pods are using the most memory"
```

### Example Outputs

**Prompt:** `kubectl ai "deploy backend with 2 replicas"`

**Generated Command:**
```bash
kubectl create deployment backend --image=todoevolutionacr.azurecr.io/backend:v1 --replicas=2
```

**Prompt:** `kubectl ai "list all pods in default namespace with their IPs"`

**Generated Command:**
```bash
kubectl get pods -o wide
```

### For Our Todo Evolution Project

```bash
# Deploy the application
kubectl ai "create a deployment for backend using image todoevolutionacr.azurecr.io/backend:v1 with env vars from secret todo-secrets"

# Check health
kubectl ai "show ready status of all deployments"

# Troubleshoot
kubectl ai "describe pod backend and show events"

# Scale for load
kubectl ai "increase backend replicas to handle more traffic"
```

---

## 2. kagent (Kubernetes AI Agent)

kagent is an intelligent Kubernetes agent that provides cluster analysis, diagnostics, and recommendations.

### Installation

```bash
# Install kagent CLI
pip install kagent

# Or with pipx
pipx install kagent

# Configure with kubeconfig
kagent init --kubeconfig ~/.kube/config
```

### Usage Examples

```bash
# Cluster health analysis
kagent analyze cluster

# Resource optimization
kagent optimize --namespace default

# Security scan
kagent security-scan

# Troubleshoot a pod
kagent diagnose pod backend-xxx-yyy

# Cost optimization
kagent cost-report

# Generate YAML from description
kagent generate "FastAPI backend with health checks and resource limits"
```

### Example Outputs

**Command:** `kagent analyze cluster`

**Output:**
```
📊 Cluster Health Report
========================
✅ Nodes: 1/1 healthy
✅ Control Plane: Running
✅ CoreDNS: 2/2 pods ready
⚠️  PodDisruptionBudgets: 0 configured
⚠️  ResourceQuotas: 0 configured

🔍 Recommendations:
1. Add PodDisruptionBudget for backend deployment
2. Configure ResourceQuota for namespace
3. Consider adding node affinity rules
```

**Command:** `kagent diagnose pod backend-xxxx`

**Output:**
```
🔬 Pod Diagnosis: backend-5d4b8c7f9-abc12
==========================================
Status: Running ✅
Restarts: 0
Age: 2h15m

Health Checks:
  Liveness: Passing (HTTP /health → 200)
  Readiness: Passing (HTTP /health → 200)

Resource Usage:
  CPU: 45m / 500m (9%)
  Memory: 128Mi / 512Mi (25%)

Events: None

✅ Pod is healthy. No issues detected.
```

### For Our Todo Evolution Project

```bash
# Analyze our deployment
kagent analyze namespace default

# Diagnose backend issues
kagent diagnose deployment backend

# Get optimization suggestions
kagent optimize deployment backend

# Generate deployment YAML
kagent generate "FastAPI backend with PostgreSQL connection, health probes, and 2 replicas"

# Security audit
kagent security-scan deployment backend
```

---

## 3. Docker AI (Gordon)

Docker Gordon is Docker Desktop's built-in AI assistant (available in Docker Desktop 4.53+).

### Enabling Gordon

1. Open Docker Desktop
2. Go to **Settings** → **Features in Development**
3. Enable **"Docker AI (Gordon)"** beta feature
4. Restart Docker Desktop

### Usage Examples

Gordon is available in the Docker Desktop GUI and CLI:

```bash
# Ask Gordon for help
docker ai "how do I build a multi-stage Dockerfile for Python?"

# Optimize Dockerfile
docker ai "analyze my backend/Dockerfile and suggest optimizations"

# Troubleshoot containers
docker ai "why is my container using so much memory?"

# Build suggestions
docker ai "what's the best base image for a FastAPI app?"

# Security recommendations
docker ai "check my Dockerfile for security issues"
```

### Example Outputs

**Prompt:** `docker ai "optimize my Python Dockerfile"`

**Gordon's Response:**
```
🤖 Docker AI Analysis

I analyzed your backend/Dockerfile. Here are my recommendations:

1. ✅ Good: Multi-stage build reduces final image size
2. ✅ Good: Using slim base image
3. ⚠️ Consider: Pin the Python version (3.13.0 instead of 3.13)
4. ⚠️ Consider: Add .dockerignore to exclude __pycache__
5. 💡 Tip: Use --no-cache-dir with pip to reduce layer size

Optimized Dockerfile:
```dockerfile
FROM python:3.13.0-slim AS builder
# ... rest of optimized Dockerfile
```
```

**Prompt:** `docker ai "explain multi-stage builds"`

**Gordon's Response:**
```
🤖 Multi-Stage Builds Explained

Multi-stage builds use multiple FROM statements to create
intermediate containers, then copy only the needed artifacts
to the final image.

Benefits:
• Smaller final images (no build tools)
• Faster deployments
• Better security (fewer attack surfaces)

Your backend/Dockerfile uses 2 stages:
1. Builder: Installs UV and dependencies
2. Runner: Only contains venv + source code

Result: ~150MB instead of ~500MB
```

### For Our Todo Evolution Project

```bash
# Analyze frontend Dockerfile
docker ai "review frontend/Dockerfile for Next.js best practices"

# Check image size
docker ai "how can I reduce my todo-frontend image size?"

# Build optimization
docker ai "should I use alpine or slim for my Python backend?"

# Container debugging
docker ai "my container exits immediately, how do I debug?"

# Compose help
docker ai "explain my docker-compose.yaml file"
```

---

## 4. Alternative: Standard Commands

If AI tools are unavailable, use these standard commands:

### kubectl Equivalents

```bash
# Deploy application
kubectl apply -f helm/todo-evolution/templates/

# Scale deployment
kubectl scale deployment backend --replicas=3

# Check pods
kubectl get pods -o wide

# View logs
kubectl logs -f deployment/backend

# Describe pod
kubectl describe pod <pod-name>

# Port forward
kubectl port-forward service/backend 8000:8000
```

### Docker Equivalents

```bash
# Build images
docker build -t backend:v1 ./backend
docker build -t frontend:v1 ./frontend

# Run container
docker run -p 8000:8000 backend:v1

# Check logs
docker logs <container-id>

# Inspect
docker inspect <container-id>
```

---

## 5. Quick Reference Card

| Task | kubectl-ai | kagent | Standard |
|------|------------|--------|----------|
| Deploy | `kubectl ai "deploy backend"` | `kagent generate "backend deployment"` | `kubectl apply -f` |
| Scale | `kubectl ai "scale to 3"` | `kagent scale backend 3` | `kubectl scale --replicas=3` |
| Debug | `kubectl ai "why is pod failing"` | `kagent diagnose pod xxx` | `kubectl describe pod` |
| Logs | `kubectl ai "show backend logs"` | `kagent logs backend` | `kubectl logs` |
| Health | `kubectl ai "cluster health"` | `kagent analyze cluster` | `kubectl get nodes` |

---

## 6. Recorded AI Tool Sessions

### Session 1: kubectl-ai Deployment

```
$ kubectl ai "deploy todo-backend with image from ACR"

🤖 Generating command...

kubectl create deployment backend \
  --image=todoevolutionacr.azurecr.io/backend:v1 \
  --port=8000

✅ Execute? [y/n]: y
deployment.apps/backend created
```

### Session 2: kagent Troubleshooting

```
$ kagent diagnose deployment backend

🔍 Analyzing deployment 'backend'...

Deployment Status:
  Desired: 1
  Current: 1
  Ready: 1
  Available: 1

Pod Health:
  backend-5d4b8c7f9-abc12: Running ✅

No issues detected. Deployment is healthy.
```

### Session 3: Gordon Dockerfile Review

```
$ docker ai "review my backend Dockerfile"

🤖 Analyzing backend/Dockerfile...

Score: 8/10 ⭐⭐⭐⭐

Strengths:
✅ Multi-stage build
✅ Health check included
✅ Non-root user would improve security

Suggestions:
1. Consider using python:3.13-slim-bookworm for stability
2. Add LABEL for maintainer info
3. Use --no-cache with pip install uv
```

---

*Evolution of Todo - Phase IV AI Tools Documentation*
