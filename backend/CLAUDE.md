# Backend Guidelines

> FastAPI with SQLModel and JWT authentication

---

## Stack

| Technology | Version |
|------------|---------|
| FastAPI | 0.115+ |
| SQLModel | 0.0.22+ |
| Asyncpg | 0.30+ |
| Python | 3.13+ |
| UV | Package manager |

---

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Pydantic settings
│   ├── database.py       # Async engine & session
│   ├── models.py         # SQLModel database models
│   ├── crud.py           # Database operations
│   ├── auth.py           # JWT verification middleware
│   └── routes/
│       ├── tasks.py      # Task CRUD endpoints
│       ├── tags.py       # Tag endpoints
│       └── chat.py       # AI chat (Phase III)
├── tests/
├── pyproject.toml
└── CLAUDE.md             # This file
```

---

## API Conventions

- All routes under `/api/{user_id}/`
- Return JSON responses
- Use Pydantic models for request/response
- Handle errors with HTTPException
- **ALL queries MUST filter by user_id**

---

## JWT Authentication

```python
from src.auth import AuthenticatedUser

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user: AuthenticatedUser,  # Injected by dependency
):
    # current_user.id is verified to match user_id
    pass
```

---

## CRUD Pattern

**CRITICAL**: All CRUD operations MUST filter by user_id:

```python
async def get_tasks(session: AsyncSession, user_id: str):
    query = select(Task).where(Task.user_id == user_id)
    result = await session.execute(query)
    return result.scalars().all()
```

---

## Database

- Connection string from: `DATABASE_URL` env variable
- Use SQLModel for all database operations
- SSL enabled for Neon PostgreSQL

---

## Commands

```bash
# Run server
uv run uvicorn src.main:app --reload

# Run tests
uv run pytest

# Lint
uv run ruff check .
```

---

## Reference Specs

- `@specs/api/rest-endpoints.md`
- `@specs/database/schema.md`
- `@specs/features/task-crud.md`

---

*Spec-Kit Plus | Evolution of Todo*
