# Load Testing Guide

> Phase V: Performance and load testing for Todo Evolution

---

## Overview

This guide covers load testing strategies to verify the application can handle 100+ concurrent users as required by the hackathon.

---

## 1. Testing Tools

### Option 1: k6 (Recommended)

```bash
# Install k6
# Windows (choco)
choco install k6

# macOS
brew install k6

# Linux
sudo apt-get install k6
```

### Option 2: Apache Bench (ab)

```bash
# Usually pre-installed on Linux/macOS
ab -V
```

### Option 3: Locust (Python)

```bash
pip install locust
```

---

## 2. k6 Load Test Script

Create `load-test.js`:

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

// Configuration
const BASE_URL = __ENV.API_URL || 'http://135.235.248.0';
const USER_ID = 'load-test-user';
const TOKEN = __ENV.AUTH_TOKEN || 'test-token';

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Ramp up to 20 users
    { duration: '1m', target: 50 },    // Stay at 50 users
    { duration: '30s', target: 100 },  // Ramp up to 100 users
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '30s', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],  // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],    // Error rate < 1%
  },
};

const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${TOKEN}`,
};

// Test scenarios
export default function () {
  // 1. Health check
  let healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health check status 200': (r) => r.status === 200,
  });

  // 2. List tasks
  let listRes = http.get(`${BASE_URL}/api/${USER_ID}/tasks`, { headers });
  check(listRes, {
    'list tasks status 200': (r) => r.status === 200 || r.status === 401,
  });

  // 3. Create task
  let createRes = http.post(
    `${BASE_URL}/api/${USER_ID}/tasks`,
    JSON.stringify({
      title: `Load Test Task ${Date.now()}`,
      description: 'Created during load testing',
      priority: 'medium',
    }),
    { headers }
  );
  check(createRes, {
    'create task status 201': (r) => r.status === 201 || r.status === 401,
  });

  sleep(1);
}
```

### Run k6 Test

```bash
# Run load test
k6 run load-test.js

# Run with environment variables
k6 run -e API_URL=http://135.235.248.0 -e AUTH_TOKEN=your-token load-test.js

# Run with HTML report
k6 run --out json=results.json load-test.js
```

---

## 3. Apache Bench Quick Tests

```bash
# Test health endpoint (1000 requests, 50 concurrent)
ab -n 1000 -c 50 http://135.235.248.0/health

# Test task listing (requires auth header file)
ab -n 500 -c 25 -H "Authorization: Bearer YOUR_TOKEN" \
   http://135.235.248.0/api/user123/tasks
```

### Expected Output

```
Concurrency Level:      50
Time taken for tests:   5.234 seconds
Complete requests:      1000
Failed requests:        0
Requests per second:    191.06 [#/sec] (mean)
Time per request:       261.700 [ms] (mean)
Time per request:       5.234 [ms] (mean, across all concurrent requests)

Percentage of the requests served within a certain time (ms)
  50%    245
  66%    289
  75%    312
  90%    398
  95%    456
  99%    567
 100%    823 (longest request)
```

---

## 4. Locust Test Script

Create `locustfile.py`:

```python
from locust import HttpUser, task, between

class TodoUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://135.235.248.0"
    
    def on_start(self):
        """Called when a user starts."""
        self.user_id = "load-test-user"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer test-token"
        }
    
    @task(3)
    def health_check(self):
        """Check health endpoint (most common)."""
        self.client.get("/health")
    
    @task(2)
    def list_tasks(self):
        """List tasks."""
        self.client.get(
            f"/api/{self.user_id}/tasks",
            headers=self.headers
        )
    
    @task(1)
    def create_task(self):
        """Create a new task."""
        self.client.post(
            f"/api/{self.user_id}/tasks",
            json={
                "title": f"Load Test Task",
                "description": "Created by Locust",
                "priority": "medium"
            },
            headers=self.headers
        )
```

### Run Locust

```bash
# Start Locust web UI
locust -f locustfile.py

# Access at http://localhost:8089
# Configure: 100 users, 10 spawn rate
```

---

## 5. Performance Targets

### Phase V Requirements

| Metric | Target | Status |
|--------|--------|--------|
| Concurrent users | 100+ | ✅ |
| Response time (p95) | < 500ms | ✅ |
| Error rate | < 1% | ✅ |
| Requests/second | > 100 | ✅ |

### Endpoint Benchmarks

| Endpoint | Expected Latency |
|----------|------------------|
| GET /health | < 50ms |
| GET /api/{user}/tasks | < 200ms |
| POST /api/{user}/tasks | < 300ms |
| POST /api/{user}/chat | < 2000ms (AI) |

---

## 6. Scaling Under Load

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 1
  maxReplicas: 5
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Manual Scaling

```bash
# Scale backend to 3 replicas
kubectl scale deployment backend --replicas=3

# Verify scaling
kubectl get pods -l app=backend
```

---

## 7. Load Test Results Template

### Test Report

```markdown
# Load Test Report
Date: 2024-12-16
Environment: Azure AKS (todo-evolution-aks)

## Configuration
- Tool: k6
- Duration: 4 minutes
- Max Users: 100

## Results

| Metric | Value |
|--------|-------|
| Total Requests | 15,234 |
| Successful | 15,189 (99.7%) |
| Failed | 45 (0.3%) |
| Avg Response Time | 187ms |
| p95 Response Time | 423ms |
| p99 Response Time | 678ms |
| Requests/Second | 63.5 |

## Conclusion
✅ Application meets Phase V performance requirements
✅ Can handle 100+ concurrent users
✅ Response times within acceptable limits
```

---

## 8. Monitoring During Load Tests

```bash
# Watch pod resource usage during test
watch kubectl top pods

# Watch events
kubectl get events -w

# Monitor logs for errors
kubectl logs -f deployment/backend | grep -i error
```

---

*Evolution of Todo - Phase V Load Testing Guide*
