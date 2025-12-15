"""Dapr Event Publisher.

Reference: @specs/features/event-driven.md
Reference: @specs/api/async-events.md

CRITICAL: Uses Dapr sidecar HTTP API, NOT direct Kafka.

✅ CORRECT: requests.post('http://localhost:3500/v1.0/publish/kafka-pubsub/task-events', json=data)
❌ FORBIDDEN: producer.send('task-events', data)
"""

import os
from datetime import datetime
from typing import Any

import httpx
from pydantic import BaseModel


class TaskEvent(BaseModel):
    """Event schema for task operations."""
    event_type: str  # TaskCreated, TaskUpdated, TaskDeleted, TaskCompleted
    task_id: int
    user_id: str
    title: str
    recurrence: str = "none"
    timestamp: datetime


class ReminderEvent(BaseModel):
    """Event schema for reminders."""
    event_type: str = "ReminderDue"
    task_id: int
    user_id: str
    title: str
    due_at: datetime


class DaprEventPublisher:
    """
    Publish events via Dapr sidecar HTTP API.
    
    CRITICAL CONSTRAINT: We MUST use Dapr HTTP API for loose coupling.
    We are FORBIDDEN from importing kafka-python or aiokafka.
    """

    def __init__(self):
        # Dapr sidecar runs on port 3500 by default
        self.dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        self.base_url = f"http://localhost:{self.dapr_port}/v1.0"
        self.pubsub_name = "kafka-pubsub"

    async def publish(
        self,
        topic: str,
        data: dict[str, Any],
    ) -> bool:
        """
        Publish event to Dapr pubsub.
        
        Uses: POST /v1.0/publish/{pubsub-name}/{topic}
        """
        url = f"{self.base_url}/publish/{self.pubsub_name}/{topic}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                )
                return response.status_code == 204
            except httpx.RequestError:
                # Dapr sidecar not available (local dev without Dapr)
                print(f"[Dapr] Sidecar not available, event not published: {data}")
                return False

    async def publish_task_event(
        self,
        event_type: str,
        task_id: int,
        user_id: str,
        title: str,
        recurrence: str = "none",
    ) -> bool:
        """Publish task event to task-events topic."""
        event = TaskEvent(
            event_type=event_type,
            task_id=task_id,
            user_id=user_id,
            title=title,
            recurrence=recurrence,
            timestamp=datetime.utcnow(),
        )
        return await self.publish("task-events", event.model_dump(mode="json"))

    async def publish_task_created(
        self,
        task_id: int,
        user_id: str,
        title: str,
    ) -> bool:
        """Publish TaskCreated event."""
        return await self.publish_task_event("TaskCreated", task_id, user_id, title)

    async def publish_task_updated(
        self,
        task_id: int,
        user_id: str,
        title: str,
    ) -> bool:
        """Publish TaskUpdated event."""
        return await self.publish_task_event("TaskUpdated", task_id, user_id, title)

    async def publish_task_deleted(
        self,
        task_id: int,
        user_id: str,
        title: str,
    ) -> bool:
        """Publish TaskDeleted event."""
        return await self.publish_task_event("TaskDeleted", task_id, user_id, title)

    async def publish_task_completed(
        self,
        task_id: int,
        user_id: str,
        title: str,
        recurrence: str = "none",
    ) -> bool:
        """Publish TaskCompleted event (includes recurrence for recurring task handler)."""
        return await self.publish_task_event(
            "TaskCompleted", task_id, user_id, title, recurrence
        )

    async def publish_reminder(
        self,
        task_id: int,
        user_id: str,
        title: str,
        due_at: datetime,
    ) -> bool:
        """Publish ReminderDue event to reminders topic."""
        event = ReminderEvent(
            task_id=task_id,
            user_id=user_id,
            title=title,
            due_at=due_at,
        )
        return await self.publish("reminders", event.model_dump(mode="json"))


# Global publisher instance
event_publisher = DaprEventPublisher()
