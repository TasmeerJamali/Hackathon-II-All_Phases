# Database Schema

> SQLModel database schema for Neon PostgreSQL.

---

## Tables

### users (managed by Better Auth)

| Column | Type | Constraints |
|--------|------|-------------|
| id | string | PRIMARY KEY |
| email | string | UNIQUE, NOT NULL |
| name | string | |
| created_at | timestamp | DEFAULT NOW() |

---

### tasks

| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | PRIMARY KEY, AUTO INCREMENT |
| user_id | string | FOREIGN KEY → users.id, NOT NULL |
| title | string(100) | NOT NULL |
| description | text | NULLABLE |
| completed | boolean | DEFAULT FALSE |
| priority | enum | "high", "medium", "low", DEFAULT "medium" |
| due_date | timestamp | NULLABLE |
| recurrence | enum | "none", "daily", "weekly", "monthly" |
| reminder_at | timestamp | NULLABLE |
| created_at | timestamp | DEFAULT NOW() |
| updated_at | timestamp | DEFAULT NOW() |

---

### tags

| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | PRIMARY KEY |
| name | string(50) | NOT NULL |
| color | string(7) | DEFAULT "#3B82F6" |

---

### task_tag_link

| Column | Type | Constraints |
|--------|------|-------------|
| task_id | integer | FOREIGN KEY → tasks.id |
| tag_id | integer | FOREIGN KEY → tags.id |

---

### conversations (Phase III)

| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | PRIMARY KEY |
| user_id | string | FOREIGN KEY → users.id |
| created_at | timestamp | DEFAULT NOW() |
| updated_at | timestamp | DEFAULT NOW() |

---

### messages (Phase III)

| Column | Type | Constraints |
|--------|------|-------------|
| id | integer | PRIMARY KEY |
| conversation_id | integer | FOREIGN KEY → conversations.id |
| user_id | string | NOT NULL |
| role | string(20) | "user" or "assistant" |
| content | text | NOT NULL |
| created_at | timestamp | DEFAULT NOW() |

---

## Indexes

| Table | Column | Purpose |
|-------|--------|---------|
| tasks | user_id | Filter by user |
| tasks | completed | Status filtering |
| tasks | priority | Priority filtering |
| messages | conversation_id | Chat history |

---

*Spec-Kit Plus | Evolution of Todo*
