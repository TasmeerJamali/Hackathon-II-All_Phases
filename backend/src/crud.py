"""CRUD operations with user_id filtering.

Reference: @backend/CLAUDE.md
CRITICAL: All CRUD operations MUST filter by user_id

Reference: @specs/features/task-crud.md
- AC-002.1: Display all tasks belonging to current user
- AC-003.4: Cannot update another user's task
- AC-004.3: Cannot delete another user's task
"""

from datetime import datetime

from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import (
    Priority,
    Tag,
    TagCreate,
    Task,
    TaskCreate,
    TaskTagLink,
    TaskUpdate,
)


# ============================================================================
# TASK CRUD - ALL QUERIES FILTER BY USER_ID
# ============================================================================


async def create_task(
    session: AsyncSession,
    task_data: TaskCreate,
    user_id: str,
) -> Task:
    """
    Create a new task for a specific user.
    
    Per AC-001.5: Task is associated with the logged-in user.
    """
    tag_ids = task_data.tag_ids
    task_dict = task_data.model_dump(exclude={"tag_ids"})

    task = Task(**task_dict, user_id=user_id)
    session.add(task)
    await session.flush()

    if tag_ids:
        for tag_id in tag_ids:
            link = TaskTagLink(task_id=task.id, tag_id=tag_id)
            session.add(link)

    await session.commit()
    await session.refresh(task)

    result = await session.execute(select(Task).where(Task.id == task.id))
    return result.scalar_one()


async def get_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
) -> Task | None:
    """
    Get a single task by ID, filtered by user_id.
    
    Returns None if task doesn't exist OR belongs to different user.
    """
    result = await session.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def get_tasks(
    session: AsyncSession,
    user_id: str,
    *,
    skip: int = 0,
    limit: int = 100,
    completed: bool | None = None,
    priority: Priority | None = None,
    search: str | None = None,
    tag_id: int | None = None,
    sort_by: str = "created_at",
    sort_desc: bool = True,
) -> list[Task]:
    """
    Get tasks with filtering, filtered by user_id.
    
    Per AC-002.1: Display all tasks belonging to current user.
    Per AC-002.4: Tasks are sorted by creation date (newest first).
    """
    # CRITICAL: Always filter by user_id
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if search:
        search_pattern = f"%{search}%"
        query = query.where(
            (Task.title.ilike(search_pattern))
            | (Task.description.ilike(search_pattern))
        )

    if tag_id is not None:
        query = query.join(TaskTagLink).where(TaskTagLink.tag_id == tag_id)

    # Sorting - default newest first per AC-002.4
    sort_column = getattr(Task, sort_by, Task.created_at)
    if sort_desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    return list(result.scalars().all())


async def update_task(
    session: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    user_id: str,
) -> Task | None:
    """
    Update a task, filtered by user_id.
    
    Per AC-003.4: Cannot update another user's task.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    update_dict = task_data.model_dump(exclude_unset=True, exclude={"tag_ids"})
    for key, value in update_dict.items():
        setattr(task, key, value)

    task.updated_at = datetime.utcnow()

    if task_data.tag_ids is not None:
        await session.execute(
            TaskTagLink.__table__.delete().where(TaskTagLink.task_id == task_id)
        )
        for tag_id in task_data.tag_ids:
            link = TaskTagLink(task_id=task_id, tag_id=tag_id)
            session.add(link)

    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(
    session: AsyncSession,
    task_id: int,
    user_id: str,
) -> bool:
    """
    Delete a task, filtered by user_id.
    
    Per AC-004.3: Cannot delete another user's task.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True


async def toggle_task_complete(
    session: AsyncSession,
    task_id: int,
    user_id: str,
) -> Task | None:
    """
    Toggle task completion, filtered by user_id.
    
    Per AC-005.4: Cannot toggle another user's task.
    """
    task = await get_task(session, task_id, user_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task


async def get_task_stats(
    session: AsyncSession,
    user_id: str,
) -> dict[str, int]:
    """Get task statistics for a user."""
    total = await session.execute(
        select(func.count(Task.id)).where(Task.user_id == user_id)
    )
    complete = await session.execute(
        select(func.count(Task.id)).where(
            Task.user_id == user_id,
            Task.completed == True  # noqa: E712
        )
    )

    total_count = total.scalar() or 0
    complete_count = complete.scalar() or 0

    return {
        "total": total_count,
        "complete": complete_count,
        "pending": total_count - complete_count,
    }


# ============================================================================
# TAG CRUD
# ============================================================================


async def create_tag(session: AsyncSession, tag_data: TagCreate) -> Tag:
    """Create a new tag."""
    tag = Tag(**tag_data.model_dump())
    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag


async def get_tags(session: AsyncSession) -> list[Tag]:
    """Get all tags."""
    result = await session.execute(select(Tag).order_by(Tag.name))
    return list(result.scalars().all())


async def delete_tag(session: AsyncSession, tag_id: int) -> bool:
    """Delete a tag by ID."""
    result = await session.execute(select(Tag).where(Tag.id == tag_id))
    tag = result.scalar_one_or_none()
    if not tag:
        return False

    await session.delete(tag)
    await session.commit()
    return True
