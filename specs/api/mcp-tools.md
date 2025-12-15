# MCP Tools Specification

> Model Context Protocol tools for AI agent integration.

---

## Tool: add_task

| Field | Value |
|-------|-------|
| Purpose | Create a new task |
| Parameters | user_id (string, required), title (string, required), description (string, optional) |
| Returns | task_id, status, title |

**Example Input:**
```json
{"user_id": "user123", "title": "Buy groceries", "description": "Milk, eggs, bread"}
```

**Example Output:**
```json
{"task_id": 5, "status": "created", "title": "Buy groceries"}
```

---

## Tool: list_tasks

| Field | Value |
|-------|-------|
| Purpose | Retrieve tasks from the list |
| Parameters | user_id (string, required), status (string, optional: "all", "pending", "completed") |
| Returns | Array of task objects |

**Example Input:**
```json
{"user_id": "user123", "status": "pending"}
```

**Example Output:**
```json
[{"id": 1, "title": "Buy groceries", "completed": false}]
```

---

## Tool: complete_task

| Field | Value |
|-------|-------|
| Purpose | Mark a task as complete |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

**Example Input:**
```json
{"user_id": "user123", "task_id": 3}
```

**Example Output:**
```json
{"task_id": 3, "status": "completed", "title": "Call mom"}
```

---

## Tool: delete_task

| Field | Value |
|-------|-------|
| Purpose | Remove a task from the list |
| Parameters | user_id (string, required), task_id (integer, required) |
| Returns | task_id, status, title |

**Example Input:**
```json
{"user_id": "user123", "task_id": 2}
```

**Example Output:**
```json
{"task_id": 2, "status": "deleted", "title": "Old task"}
```

---

## Tool: update_task

| Field | Value |
|-------|-------|
| Purpose | Modify task title or description |
| Parameters | user_id (string, required), task_id (integer, required), title (string, optional), description (string, optional) |
| Returns | task_id, status, title |

**Example Input:**
```json
{"user_id": "user123", "task_id": 1, "title": "Buy groceries and fruits"}
```

**Example Output:**
```json
{"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
```

---

*Spec-Kit Plus | Evolution of Todo*
