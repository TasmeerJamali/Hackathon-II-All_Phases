# Feature: Task CRUD Operations

> Specification for core todo task management across all phases.

---

## User Stories

### US-001: Add Task
**As a** user  
**I want to** create a new task with a title and description  
**So that** I can track things I need to do

### US-002: View Tasks
**As a** user  
**I want to** see a list of all my tasks with their status  
**So that** I can understand what needs to be done

### US-003: Update Task
**As a** user  
**I want to** modify a task's title or description  
**So that** I can correct mistakes or add more detail

### US-004: Delete Task
**As a** user  
**I want to** remove a task from my list  
**So that** I can clean up completed or cancelled items

### US-005: Mark Task Complete
**As a** user  
**I want to** mark a task as complete or incomplete  
**So that** I can track my progress

---

## Acceptance Criteria

### AC-001: Create Task
| Criterion | Description |
|-----------|-------------|
| AC-001.1 | Title is required (1-200 characters) |
| AC-001.2 | Description is optional (max 1000 characters) |
| AC-001.3 | Task is created with status "pending" |
| AC-001.4 | Task is assigned a unique ID |
| AC-001.5 | Task is associated with the logged-in user (Phase II+) |
| AC-001.6 | System confirms successful creation |

### AC-002: View Tasks
| Criterion | Description |
|-----------|-------------|
| AC-002.1 | Display all tasks belonging to current user |
| AC-002.2 | Show task ID, title, and status indicator |
| AC-002.3 | Status shows ✅ for complete, ❌ for pending |
| AC-002.4 | Tasks are sorted by creation date (newest first) |
| AC-002.5 | Empty state shows "No tasks found" message |

### AC-003: Update Task
| Criterion | Description |
|-----------|-------------|
| AC-003.1 | Can update title (1-200 characters) |
| AC-003.2 | Can update description (max 1000 characters) |
| AC-003.3 | Cannot update task that doesn't exist |
| AC-003.4 | Cannot update another user's task (Phase II+) |
| AC-003.5 | System confirms successful update |

### AC-004: Delete Task
| Criterion | Description |
|-----------|-------------|
| AC-004.1 | Task is permanently removed |
| AC-004.2 | Cannot delete task that doesn't exist |
| AC-004.3 | Cannot delete another user's task (Phase II+) |
| AC-004.4 | System confirms successful deletion |

### AC-005: Mark Complete
| Criterion | Description |
|-----------|-------------|
| AC-005.1 | Toggle task between complete/incomplete |
| AC-005.2 | Status is visually indicated |
| AC-005.3 | Cannot toggle task that doesn't exist |
| AC-005.4 | Cannot toggle another user's task (Phase II+) |
| AC-005.5 | System confirms status change |

---

## Technical Constraints

### Phase I (Console)
- In-memory storage (Python dict)
- No database or file I/O
- Single user (no authentication)

### Phase II+ (Web)
- SQLModel ORM with Neon PostgreSQL
- JWT authentication required
- All operations filtered by user_id

---

## API Endpoints (Phase II+)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

---

*Spec-Kit Plus | Evolution of Todo*
