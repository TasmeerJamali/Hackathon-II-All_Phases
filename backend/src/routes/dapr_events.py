"""Dapr Event Consumers and Handlers.

Reference: @specs/features/event-driven.md
Reference: @specs/api/async-events.md

Implements ALL 5 Dapr Building Blocks:
1. Pub/Sub - Subscription declaration endpoint (GET /dapr/subscribe)
2. State Management - Used via statestore component
3. Bindings - Cron binding handler (POST /reminder-cron)
4. Service Invocation - Call other services via Dapr
5. Secrets Management - Retrieve secrets via Dapr API

Event handlers (POST /events/task-events)
Audit logging
Recurring task creation
Jobs API handler (POST /jobs/callback)
"""

from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Request
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import async_session_maker
from src.events import event_publisher
from src.models import Task, RecurrenceType
from src.dapr_client import service_client, secrets_client, jobs_client

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


# ============================================================================
# DAPR JOBS API CALLBACK
# Triggered when a scheduled job fires
# Building Block 4b: Jobs/Scheduling
# ============================================================================


@router.post("/jobs/callback")
async def jobs_callback_handler(request: Request) -> dict[str, str]:
    """
    Handle Dapr Jobs API callbacks.
    
    This endpoint is called when a scheduled job triggers.
    Used for precise reminder scheduling (instead of cron polling).
    """
    try:
        job_data = await request.json()
    except Exception:
        return {"status": "ERROR", "message": "Invalid JSON"}

    job_type = job_data.get("type", "unknown")
    task_id = job_data.get("task_id")
    user_id = job_data.get("user_id")
    title = job_data.get("title")

    print(f"[JOBS] Callback received: {job_type} | Task #{task_id} | User: {user_id}")

    if job_type == "reminder":
        # Use Service Invocation to notify (Building Block 4)
        await service_client.invoke_notification_service(
            task_id=task_id,
            user_id=user_id,
            title=title,
            message=f"Reminder: {title} is due!",
        )
        print(f"[JOBS] Reminder sent for task #{task_id}")

    return {"status": "SUCCESS", "job_type": job_type}


# ============================================================================
# DAPR SERVICE INVOCATION ENDPOINT
# Can be called by other services via Dapr
# Building Block 4: Service Invocation
# ============================================================================


@router.post("/send-notification")
async def send_notification_handler(request: Request) -> dict[str, str]:
    """
    Handle notification requests via Dapr Service Invocation.
    
    Other services can call this via:
    POST /v1.0/invoke/backend/method/send-notification
    """
    try:
        data = await request.json()
    except Exception:
        return {"status": "ERROR", "message": "Invalid JSON"}

    task_id = data.get("task_id")
    user_id = data.get("user_id")
    title = data.get("title")
    message = data.get("message")

    # In production, this would send push notification, email, etc.
    print(f"[NOTIFICATION] Task #{task_id} for {user_id}: {message}")

    return {"status": "SENT", "task_id": str(task_id), "title": title}


# ============================================================================
# DAPR SECRETS EXAMPLE ENDPOINT
# Demonstrates Dapr Secrets Management (Building Block 5)
# ============================================================================


@router.get("/dapr/secrets-test")
async def test_dapr_secrets() -> dict[str, str]:
    """
    Test Dapr Secrets Management.
    
    This endpoint demonstrates retrieving secrets via Dapr API.
    """
    db_url = await secrets_client.get_database_url()
    has_openai = bool(await secrets_client.get_openai_key())
    has_auth = bool(await secrets_client.get_auth_secret())

    return {
        "status": "OK",
        "database_configured": "yes" if db_url else "no (fallback to env)",
        "openai_configured": "yes" if has_openai else "no (fallback to env)",
        "auth_configured": "yes" if has_auth else "no (fallback to env)",
    }

