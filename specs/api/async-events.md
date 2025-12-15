# Async Events API

> Dapr pub/sub and binding specifications for Phase V.

---

## Dapr Sidecar Endpoints

Base URL: `http://localhost:3500` (Dapr sidecar port)

---

## Publishing Events

### Publish to topic
```
POST /v1.0/publish/{pubsub-name}/{topic}
```

**Example: Publish TaskCreated event**
```bash
POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events
Content-Type: application/json

{
  "event_type": "TaskCreated",
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Buy groceries",
  "timestamp": "2024-12-10T00:00:00Z"
}
```

---

## Subscribing to Events

### Declare subscriptions
FastAPI must expose this endpoint for Dapr to discover subscriptions:

```
GET /dapr/subscribe
```

**Response:**
```json
[
  {
    "pubsubname": "kafka-pubsub",
    "topic": "task-events",
    "route": "/events/task-events"
  }
]
```

### Event handler endpoint
```
POST /events/task-events
```

Dapr will POST events to this endpoint.

---

## Cron Binding

### Binding triggers this endpoint every 5 minutes:
```
POST /reminder-cron
```

**Response:** 200 OK

---

## Dapr Component YAML Schemas

### pubsub.kafka
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "redpanda:9092"
    - name: consumerGroup
      value: "todo-backend"
    - name: authType
      value: "none"
```

### state.postgresql
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: todo-secrets
        key: DATABASE_URL
```

### bindings.cron
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "*/5 * * * *"
    - name: direction
      value: "input"
```

---

*Spec-Kit Plus | Evolution of Todo*
