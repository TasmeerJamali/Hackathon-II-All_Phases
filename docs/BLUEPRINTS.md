# Cloud-Native Blueprints

> Bonus 2: +200 Points - Infrastructure as Code blueprints for repeatable deployments

---

## Overview

This project includes reusable cloud-native blueprints that can be deployed to any Kubernetes cluster.

---

## Blueprint 1: Todo App Blueprint

### Purpose
Complete deployment blueprint for a full-stack todo application with event-driven architecture.

### Components
- Frontend (Next.js)
- Backend (FastAPI)
- Message Broker (Redpanda/Kafka)
- Dapr Runtime

### Usage

```bash
# Deploy the blueprint
./blueprints/todo-app/deploy.sh \
  --cluster-name todo-production \
  --database-url "postgresql://..." \
  --domain todo.example.com
```

### Files
```
blueprints/todo-app/
├── deploy.sh           # Main deployment script
├── values-template.yaml # Configurable values
├── kustomization.yaml  # Kustomize configuration
└── README.md           # Blueprint documentation
```

---

## Blueprint 2: Event-Driven Microservice Blueprint

### Purpose
Blueprint for deploying event-driven microservices with Dapr.

### Components
- Service Deployment
- Dapr Sidecar Configuration
- Pub/Sub Component
- State Store Component

### Usage

```bash
# Generate microservice from blueprint
./blueprints/event-service/generate.sh \
  --name notification-service \
  --topics "task-events,reminders" \
  --output-dir ./services/notification
```

---

## Blueprint Files

### Blueprint 1: Todo App

Location: `blueprints/todo-app/`
