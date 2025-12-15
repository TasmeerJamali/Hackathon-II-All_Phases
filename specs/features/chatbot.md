# Feature: AI Chatbot

> Specification for Phase III AI-powered natural language todo management.

---

## User Stories

### US-CHAT-001: Natural Language Task Creation
**As a** user  
**I want to** say "Add a task to buy groceries"  
**So that** the AI creates the task for me

### US-CHAT-002: Conversational Task Listing
**As a** user  
**I want to** ask "What's pending?"  
**So that** the AI shows my incomplete tasks

### US-CHAT-003: Voice-like Commands
**As a** user  
**I want to** say "Mark task 3 as done"  
**So that** the AI completes the task

---

## Acceptance Criteria

### AC-CHAT-001: Natural Language Understanding
| Criterion | Description |
|-----------|-------------|
| AC-CHAT-001.1 | "Add task to X" → calls add_task tool |
| AC-CHAT-001.2 | "Show my tasks" → calls list_tasks(status="all") |
| AC-CHAT-001.3 | "What's pending?" → calls list_tasks(status="pending") |
| AC-CHAT-001.4 | "Mark task X as done" → calls complete_task |
| AC-CHAT-001.5 | "Delete task X" → calls delete_task |

### AC-CHAT-002: Stateless Architecture
| Criterion | Description |
|-----------|-------------|
| AC-CHAT-002.1 | Server holds NO state between requests |
| AC-CHAT-002.2 | Conversation history stored in database |
| AC-CHAT-002.3 | Each request fetches history from DB |

### AC-CHAT-003: MCP Tools
| Criterion | Description |
|-----------|-------------|
| AC-CHAT-003.1 | add_task(user_id, title, description) |
| AC-CHAT-003.2 | list_tasks(user_id, status) |
| AC-CHAT-003.3 | complete_task(user_id, task_id) |
| AC-CHAT-003.4 | delete_task(user_id, task_id) |
| AC-CHAT-003.5 | update_task(user_id, task_id, title, description) |

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | OpenAI ChatKit |
| AI Logic | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| Database | Neon PostgreSQL |

---

## API Endpoint

```
POST /api/{user_id}/chat
```

**Request:**
```json
{
  "conversation_id": 123,  // optional
  "message": "Add a task to buy milk"
}
```

**Response:**
```json
{
  "conversation_id": 123,
  "response": "✅ Created task #5: 'Buy milk'",
  "tool_calls": ["add_task"]
}
```

---

*Spec-Kit Plus | Evolution of Todo*
