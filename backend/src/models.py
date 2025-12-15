"""SQLModel database models.

Reference: @specs/database/schema.md
- Task model with user_id field (AC-001.5)
- Title max 100 chars, description max 1000 (AC-001.1, AC-001.2)
"""

from datetime import datetime
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class Priority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecurrenceType(str, Enum):
    """Task recurrence types (Phase V)."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskTagLink(SQLModel, table=True):
    """Many-to-many link between Task and Tag."""
    __tablename__ = "task_tag_link"
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class TagBase(SQLModel):
    """Base tag model."""
    name: str = Field(max_length=50, index=True)
    color: str = Field(default="#3B82F6", max_length=7)


class Tag(TagBase, table=True):
    """Tag database model."""
    __tablename__ = "tag"
    id: int | None = Field(default=None, primary_key=True)
    tasks: list["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)


class TaskBase(SQLModel):
    """Base task model.
    
    Per specs/features/task-crud.md:
    - AC-001.1: Title is required (1-200 characters)
    - AC-001.2: Description is optional (max 1000 characters)
    """
    title: str = Field(max_length=200, min_length=1, index=True)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: Priority = Field(default=Priority.MEDIUM, index=True)
    due_date: datetime | None = Field(default=None)
    recurrence: RecurrenceType = Field(default=RecurrenceType.NONE)
    reminder_at: datetime | None = Field(default=None)


class Task(TaskBase, table=True):
    """Task database model.
    
    Per specs/features/task-crud.md:
    - AC-001.4: Task is assigned a unique ID
    - AC-001.5: Task is associated with the logged-in user
    """
    __tablename__ = "task"
    
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)  # CRITICAL: User who owns this task
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    tags: list[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================


class TagRead(TagBase):
    """Tag response model."""
    id: int


class TagCreate(SQLModel):
    """Tag creation model."""
    name: str = Field(max_length=50)
    color: str = Field(default="#3B82F6", max_length=7)


class TaskRead(TaskBase):
    """Task response model."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskReadWithTags(TaskRead):
    """Task response with tags included."""
    tags: list[TagRead] = []


class TaskCreate(SQLModel):
    """Task creation model.
    
    Per specs/features/task-crud.md:
    - AC-001.1: Title is required (1-200 characters)
    - AC-001.2: Description is optional (max 1000 characters)
    """
    title: str = Field(max_length=200, min_length=1)
    description: str = Field(default="", max_length=1000)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: datetime | None = None
    recurrence: RecurrenceType = Field(default=RecurrenceType.NONE)
    reminder_at: datetime | None = None
    tag_ids: list[int] = Field(default_factory=list)


class TaskUpdate(SQLModel):
    """Task update model.
    
    Per specs/features/task-crud.md:
    - AC-003.1: Can update title (1-200 characters)
    - AC-003.2: Can update description (max 1000 characters)
    """
    title: str | None = Field(default=None, max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    completed: bool | None = None
    priority: Priority | None = None
    due_date: datetime | None = None
    recurrence: RecurrenceType | None = None
    reminder_at: datetime | None = None
    tag_ids: list[int] | None = None


# ============================================================================
# PHASE III: CONVERSATION MODELS
# Per specs/features/chatbot.md AC-CHAT-002.2: Conversation history stored in DB
# ============================================================================


class Conversation(SQLModel, table=True):
    """Chat conversation/session.
    
    Per AC-CHAT-002.2: Conversation history stored in database.
    """
    __tablename__ = "conversation"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """Individual chat message.
    
    Per AC-CHAT-002.3: Each request fetches history from DB.
    """
    __tablename__ = "message"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: str = Field(index=True)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str  # No max_length for chat messages
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Conversation | None = Relationship(back_populates="messages")


# ============================================================================
# CHAT API MODELS
# Per specs/api/rest-endpoints.md POST /api/{user_id}/chat
# ============================================================================


class ChatRequest(SQLModel):
    """Chat API request."""
    conversation_id: int | None = None
    message: str


class ChatResponse(SQLModel):
    """Chat API response."""
    conversation_id: int
    response: str
    tool_calls: list[str] = Field(default_factory=list)
