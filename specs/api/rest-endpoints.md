# REST API Endpoints

> API specification for all backend endpoints.

---

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.todo.example.com`

---

## Authentication

All endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

---

## Endpoints

### GET /api/{user_id}/tasks
List all tasks for authenticated user.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| status | string | "all", "pending", "completed" |
| priority | string | "high", "medium", "low" |
| sort | string | "created", "title", "due_date" |

**Response:** Array of Task objects

---

### POST /api/{user_id}/tasks
Create a new task.

**Request Body:**
```json
{
  "title": "string (required)",
  "description": "string (optional)",
  "priority": "medium",
  "due_date": "2024-12-31T00:00:00Z"
}
```

**Response:** Created Task object (201)

---

### GET /api/{user_id}/tasks/{id}
Get single task details.

**Response:** Task object or 404

---

### PUT /api/{user_id}/tasks/{id}
Update a task.

**Request Body:**
```json
{
  "title": "string (optional)",
  "description": "string (optional)",
  "priority": "string (optional)"
}
```

**Response:** Updated Task object

---

### DELETE /api/{user_id}/tasks/{id}
Delete a task.

**Response:** 204 No Content

---

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status.

**Response:** Updated Task object

---

## Chat Endpoint (Phase III)

### POST /api/{user_id}/chat
Send message to AI assistant.

**Request:**
```json
{
  "conversation_id": 123,
  "message": "Add a task to buy groceries"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "Created task #5: Buy groceries",
  "tool_calls": ["add_task"]
}
```

---

*Spec-Kit Plus | Evolution of Todo*
