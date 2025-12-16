# Monitoring & Observability Guide

> Phase V: Complete monitoring, logging, and observability for Todo Evolution

---

## Overview

This guide covers the monitoring stack for the Evolution of Todo application deployed on Kubernetes.

---

## 1. Application Health Endpoints

### Backend Health Check

```bash
# Check backend health
curl http://135.235.248.0/health

# Expected response
{"status": "healthy", "phase": "V"}
```

### Kubernetes Pod Health

```bash
# Check pod status
kubectl get pods -o wide

# Check pod health details
kubectl describe pod backend-xxxxx

# View liveness/readiness probe status
kubectl get pods -o jsonpath='{.items[*].status.conditions}'
```

---

## 2. Logging

### View Application Logs

```bash
# Backend logs
kubectl logs -f deployment/backend

# Frontend logs (if deployed to K8s)
kubectl logs -f deployment/frontend

# Dapr sidecar logs
kubectl logs -f deployment/backend -c daprd

# All pods in namespace
kubectl logs -f -l app=backend
```

### Structured Log Format

The backend uses structured logging:

```python
# Example log output
[2024-12-16 10:30:45] INFO  | TaskCreated | Task #123 | User: user_abc | Title: Buy groceries
[2024-12-16 10:30:46] INFO  | [AUDIT] TaskCreated | Task #123 | User: user_abc
[2024-12-16 10:35:00] INFO  | [CRON] Processed 3 reminder(s)
[2024-12-16 10:35:01] INFO  | [RECURRING] Created next task #124: 'Daily standup' due 2024-12-17
```

### Log Levels

| Level | Usage |
|-------|-------|
| DEBUG | Detailed debugging information |
| INFO | General operational information |
| WARNING | Warning conditions |
| ERROR | Error conditions |
| CRITICAL | Critical failures |

---

## 3. Metrics

### Kubernetes Resource Metrics

```bash
# Enable metrics server in Minikube
minikube addons enable metrics-server

# View node metrics
kubectl top nodes

# View pod metrics
kubectl top pods

# View specific pod metrics
kubectl top pod backend-xxxxx
```

### Expected Output

```
NAME                       CPU(cores)   MEMORY(bytes)
backend-5d4b8c7f9-abc12    45m          128Mi
frontend-7c8d9e1f2-xyz34   30m          96Mi
```

### Application Metrics

The backend exposes key metrics:

| Metric | Description |
|--------|-------------|
| Request count | Total API requests |
| Response time | Average response latency |
| Error rate | 4xx/5xx error percentage |
| Active connections | Current open connections |

---

## 4. Events

### Kubernetes Events

```bash
# View all events
kubectl get events --sort-by='.lastTimestamp'

# View events for specific deployment
kubectl get events --field-selector involvedObject.name=backend

# Watch events in real-time
kubectl get events -w
```

### Event Types to Monitor

| Event | Significance |
|-------|--------------|
| Scheduled | Pod scheduled to node |
| Pulled | Container image pulled |
| Started | Container started |
| Unhealthy | Health check failed |
| Killing | Pod being terminated |
| BackOff | Container restart backoff |

---

## 5. Dapr Observability

### Dapr Dashboard

```bash
# Start Dapr dashboard
dapr dashboard -k

# Access at http://localhost:8080
```

### Dapr Metrics

```bash
# View Dapr sidecar metrics
kubectl exec -it deployment/backend -c daprd -- wget -qO- http://localhost:9090/metrics
```

### Dapr Logs

```bash
# View Dapr system logs
kubectl logs -n dapr-system -l app=dapr-operator

# View Dapr sidecar injector logs
kubectl logs -n dapr-system -l app=dapr-sidecar-injector
```

---

## 6. Kafka/Redpanda Monitoring

### Topic Status

```bash
# Using Redpanda Console (docker-compose)
# Access at http://localhost:8082

# Using rpk CLI
kubectl exec -it redpanda-0 -- rpk topic list
kubectl exec -it redpanda-0 -- rpk topic describe task-events
```

### Consumer Lag

```bash
# Check consumer group lag
kubectl exec -it redpanda-0 -- rpk group describe todo-backend
```

### Expected Metrics

| Metric | Healthy Value |
|--------|---------------|
| Consumer lag | < 100 messages |
| Partition count | 3+ per topic |
| Replication factor | 1 (dev), 3 (prod) |

---

## 7. Alerting Rules

### Critical Alerts

| Alert | Condition | Action |
|-------|-----------|--------|
| PodCrashLoopBackOff | Restarts > 5 in 10min | Check logs, fix config |
| HighMemoryUsage | Memory > 80% limit | Scale or optimize |
| HighCPUUsage | CPU > 90% limit | Scale horizontally |
| HealthCheckFailed | 3+ consecutive fails | Restart pod |
| KafkaConsumerLag | Lag > 1000 | Scale consumers |

### Alert Configuration (Prometheus)

```yaml
groups:
  - name: todo-evolution
    rules:
      - alert: BackendDown
        expr: up{app="backend"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Backend is down"
          
      - alert: HighErrorRate
        expr: rate(http_request_errors_total[5m]) > 0.1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
```

---

## 8. Dashboards

### Kubernetes Dashboard

```bash
# Enable dashboard in Minikube
minikube dashboard

# Access via browser
```

### Custom Metrics Dashboard

Key panels to include:

1. **Overview Panel**
   - Total pods running
   - Total requests/minute
   - Error rate percentage

2. **Backend Panel**
   - Task creation rate
   - Chat requests/minute
   - Database query time

3. **Event-Driven Panel**
   - Kafka message throughput
   - Consumer lag
   - Event processing time

4. **Infrastructure Panel**
   - CPU/Memory usage
   - Network I/O
   - Disk usage

---

## 9. Troubleshooting Commands

### Quick Diagnostics

```bash
# Get cluster health summary
kubectl get componentstatus

# Check all resources
kubectl get all

# Describe problematic pod
kubectl describe pod <pod-name>

# Get pod logs with errors only
kubectl logs <pod-name> | grep -i error

# Check resource usage
kubectl top pods --sort-by=memory

# Check events for issues
kubectl get events --field-selector type=Warning
```

### Common Issues

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| ImagePullBackOff | Wrong image or no access | Fix image name or add pull secret |
| CrashLoopBackOff | App crashing on start | Check logs for startup errors |
| Pending | No resources or node issues | Check node status | 
| OOMKilled | Memory limit exceeded | Increase memory limit |

---

## 10. Production Recommendations

### Logging Stack (ELK)

```yaml
# Recommended for production
- Elasticsearch: Log storage
- Logstash: Log processing
- Kibana: Visualization
- Filebeat: Log collection
```

### Monitoring Stack (Prometheus/Grafana)

```yaml
# Recommended for production
- Prometheus: Metrics collection
- Grafana: Dashboards
- AlertManager: Alerting
- Node Exporter: Node metrics
```

### Tracing (Jaeger/Zipkin)

```yaml
# Recommended for distributed tracing
- Jaeger: Trace collection and UI
- OpenTelemetry: Instrumentation
```

---

*Evolution of Todo - Phase V Monitoring Guide*
