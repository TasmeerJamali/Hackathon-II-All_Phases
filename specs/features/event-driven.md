# Feature: Event-Driven Architecture

> Phase V specification for distributed event-driven todo system using Dapr.

---

## Overview

Transform the monolithic CRUD app into a loosely-coupled distributed system
using Dapr (Distributed Application Runtime) to abstract infrastructure.

---

## Architecture

```
┌─────────────┐     Dapr HTTP      ┌─────────────┐      ┌─────────────┐
│   FastAPI   │ ──────────────────▶│   Dapr      │ ───▶ │  Redpanda   │
│   Backend   │    :3500/publish   │   Sidecar   │      │   (Kafka)   │
└─────────────┘                    └─────────────┘      └─────────────┘
                                          │
                                          ▼
                                   ┌─────────────┐
                                   │  Consumer   │
                                   │  Services   │
                                   └─────────────┘
```

---

## Critical Constraint

**FORBIDDEN**: Importing `kafka-python` or `aiokafka` directly.

**REQUIRED**: Use Dapr Sidecar HTTP API:
```python
# ✅ CORRECT - Dapr abstraction
requests.post(
    'http://localhost:3500/v1.0/publish/kafka-pubsub/task-events',
    json=event_data
)

# ❌ INCORRECT - Direct Kafka coupling
producer.send('task-events', data)
```

---

## Topics

### topic: task-events
| Field | Description |
|-------|-------------|
| Purpose | Log all task CRUD operations |
| Events | TaskCreated, TaskUpdated, TaskDeleted, TaskCompleted |
| Consumers | Audit Service, Recurring Task Service |

### topic: reminders
| Field | Description |
|-------|-------------|
| Purpose | Notification triggers for due tasks |
| Events | ReminderDue |
| Consumers | Notification Service |

---

## Event Schemas

### TaskCreated
```json
{
  "event_type": "TaskCreated",
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Buy groceries",
  "timestamp": "2024-12-10T00:00:00Z"
}
```

### TaskCompleted
```json
{
  "event_type": "TaskCompleted",
  "task_id": 123,
  "user_id": "user_abc",
  "title": "Buy groceries",
  "recurrence": "daily",
  "timestamp": "2024-12-10T00:00:00Z"
}
```

### ReminderDue
```json
{
  "event_type": "ReminderDue",
  "task_id": 456,
  "user_id": "user_abc",
  "title": "Call mom",
  "due_at": "2024-12-10T15:00:00Z"
}
```

---

## Dapr Components

### 1. pubsub.kafka (Redpanda)
Pub/Sub component for event streaming.

### 2. state.postgresql  
State store using existing Neon database.

### 3. bindings.cron
Input binding that triggers reminder checks every 5 minutes.

---

## Consumer Services

### Audit Service
- Subscribes to: `task-events`
- Action: Log all events to console and/or database

### Recurring Task Service
- Subscribes to: `task-events` (TaskCompleted only)
- Action: If `recurrence != "none"`, create next task instance

### Reminder Service
- Triggered by: `bindings.cron` (every 5 min)
- Action: Query tasks where `reminder_at <= now()`, publish to `reminders`

---

*Spec-Kit Plus | Evolution of Todo*
