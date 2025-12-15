"""Dapr Event Consumers and Handlers.

Reference: @specs/features/event-driven.md
Reference: @specs/api/async-events.md

Implements:
1. Subscription declaration endpoint (GET /dapr/subscribe)
2. Event handlers (POST /events/task-events)
3. Cron binding handler (POST /reminder-cron)
4. Audit logging
5. Recurring task creation
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import async_session_maker
from src.events import event_publisher
from src.models import Task, RecurrenceType

router = APIRouter(tags=["Dapr Events"])


# ============================================================================
# DAPR SUBSCRIPTION DECLARATION
# Dapr calls this endpoint to discover topic subscriptions
# ============================================================================


@router.get("/dapr/subscribe")
async def dapr_subscribe() -> list[dict[str, str]]:
    """
    Declare subscriptions for Dapr.
    
    Dapr will call this endpoint on startup to discover
    which topics this service wants to subscribe to.
    """
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "task-events",
            "route": "/events/task-events",
        },
        {
            "pubsubname": "kafka-pubsub",
            "topic": "reminders",
            "route": "/events/reminders",
        },
    ]


# ============================================================================
# EVENT HANDLERS
# ============================================================================


@router.post("/events/task-events")
async def handle_task_events(request: Request) -> dict[str, str]:
    """
    Handle events from task-events topic.
    
    This handler implements:
    1. AUDIT LOG - Logs all events (per hackathon requirement)
    2. RECURRING TASKS - Creates next instance on TaskCompleted
    """
    try:
        event = await request.json()
    except Exception:
        return {"status": "ERROR", "message": "Invalid JSON"}

    event_type = event.get("event_type", "Unknown")
    task_id = event.get("task_id")
    user_id = event.get("user_id")
    title = event.get("title")
    recurrence = event.get("recurrence", "none")
    timestamp = event.get("timestamp")

    # ==========================================
    # AUDIT LOG (Required by hackathon)
    # ==========================================
    print(f"[AUDIT] {timestamp} | {event_type} | Task #{task_id} | User: {user_id} | Title: {title}")

    # ==========================================
    # RECURRING TASK SERVICE
    # ==========================================
    if event_type == "TaskCompleted" and recurrence != "none":
        await create_next_recurring_task(
            user_id=user_id,
            title=title,
            recurrence=recurrence,
        )

    return {"status": "SUCCESS"}


@router.post("/events/reminders")
async def handle_reminder_events(request: Request) -> dict[str, str]:
    """Handle events from reminders topic."""
    try:
        event = await request.json()
    except Exception:
        return {"status": "ERROR", "message": "Invalid JSON"}

    task_id = event.get("task_id")
    user_id = event.get("user_id")
    title = event.get("title")
    due_at = event.get("due_at")

    # Log the reminder (in production, this would send push notification)
    print(f"[REMINDER] Task #{task_id} for {user_id}: '{title}' is due at {due_at}")

    return {"status": "SUCCESS"}


# ============================================================================
# CRON BINDING HANDLER
# Dapr triggers this every 5 minutes per bindings.cron component
# ============================================================================


@router.post("/reminder-cron")
async def reminder_cron_handler() -> dict[str, str]:
    """
    Cron binding handler - triggered every 5 minutes by Dapr.
    
    Per specs/api/async-events.md:
    - Queries tasks where reminder_at <= now()
    - Publishes ReminderDue events
    """
    now = datetime.utcnow()
    reminder_count = 0

    async with async_session_maker() as session:
        # Find tasks with reminders due
        result = await session.execute(
            select(Task).where(
                Task.reminder_at <= now,
                Task.completed == False,  # noqa: E712
            )
        )
        tasks_due = result.scalars().all()

        for task in tasks_due:
            # Publish reminder event
            await event_publisher.publish_reminder(
                task_id=task.id,
                user_id=task.user_id,
                title=task.title,
                due_at=task.reminder_at,
            )
            reminder_count += 1

            # Clear the reminder (so it doesn't fire again)
            task.reminder_at = None

        if tasks_due:
            await session.commit()

    print(f"[CRON] Processed {reminder_count} reminder(s)")
    return {"status": "SUCCESS", "reminders_sent": str(reminder_count)}


# ============================================================================
# RECURRING TASK SERVICE
# Creates next task instance when a recurring task is completed
# ============================================================================


async def create_next_recurring_task(
    user_id: str,
    title: str,
    recurrence: str,
) -> None:
    """
    Create the next instance of a recurring task.
    
    Per specs/features/event-driven.md:
    When TaskCompleted event is received for a recurring task,
    automatically create the next task instance.
    """
    # Calculate next due date based on recurrence
    now = datetime.utcnow()
    
    if recurrence == "daily":
        next_due = now + timedelta(days=1)
    elif recurrence == "weekly":
        next_due = now + timedelta(weeks=1)
    elif recurrence == "monthly":
        next_due = now + timedelta(days=30)
    else:
        return  # Unknown recurrence, skip

    async with async_session_maker() as session:
        new_task = Task(
            user_id=user_id,
            title=title,
            description=f"Recurring from: {now.date()}",
            completed=False,
            recurrence=RecurrenceType(recurrence),
            due_date=next_due,
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)

        print(f"[RECURRING] Created next task #{new_task.id}: '{title}' due {next_due.date()}")

        # Publish event for the new task
        await event_publisher.publish_task_created(
            task_id=new_task.id,
            user_id=user_id,
            title=title,
        )
