"""Dapr Service Invocation and Secrets Management.

Reference: @specs/features/event-driven.md
Implements Dapr Building Blocks 4 & 5:
- Service Invocation: Service-to-service calls via Dapr
- Secrets Management: Retrieve secrets via Dapr Secrets API
"""

import os
from typing import Any

import httpx


class DaprServiceClient:
    """
    Dapr Service Invocation client.
    
    Building Block 4: Service Invocation
    Enables service-to-service calls with mTLS, retry, and load balancing.
    """

    def __init__(self):
        self.dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        self.base_url = f"http://localhost:{self.dapr_port}/v1.0"

    async def invoke(
        self,
        app_id: str,
        method: str,
        data: dict[str, Any] | None = None,
        http_method: str = "POST",
    ) -> dict[str, Any]:
        """
        Invoke a method on another service via Dapr.
        
        Uses: POST /v1.0/invoke/{app-id}/method/{method-name}
        
        Example:
            await service_client.invoke("notification-service", "send-reminder", {"task_id": 123})
        """
        url = f"{self.base_url}/invoke/{app_id}/method/{method}"

        async with httpx.AsyncClient() as client:
            try:
                if http_method == "GET":
                    response = await client.get(url)
                else:
                    response = await client.post(
                        url,
                        json=data or {},
                        headers={"Content-Type": "application/json"},
                    )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"error": f"Service call failed: {response.status_code}"}
            except httpx.RequestError as e:
                print(f"[Dapr] Service invocation failed: {e}")
                return {"error": str(e)}

    async def invoke_notification_service(
        self,
        task_id: int,
        user_id: str,
        title: str,
        message: str,
    ) -> dict[str, Any]:
        """Invoke notification service to send a reminder."""
        return await self.invoke(
            app_id="notification-service",
            method="send-notification",
            data={
                "task_id": task_id,
                "user_id": user_id,
                "title": title,
                "message": message,
            },
        )


class DaprSecretsClient:
    """
    Dapr Secrets Management client.
    
    Building Block 5: Secrets Management
    Retrieves secrets from configured secret stores (Kubernetes, Vault, etc.)
    """

    def __init__(self):
        self.dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        self.base_url = f"http://localhost:{self.dapr_port}/v1.0"
        self.store_name = "kubernetes-secrets"

    async def get_secret(self, secret_name: str) -> dict[str, str]:
        """
        Get a secret from the Dapr secret store.
        
        Uses: GET /v1.0/secrets/{secret-store-name}/{secret-name}
        """
        url = f"{self.base_url}/secrets/{self.store_name}/{secret_name}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"[Dapr] Secret not found: {secret_name}")
                    return {}
            except httpx.RequestError as e:
                print(f"[Dapr] Secrets API not available: {e}")
                return {}

    async def get_database_url(self) -> str:
        """Get DATABASE_URL from Dapr secrets."""
        secrets = await self.get_secret("todo-secrets")
        return secrets.get("DATABASE_URL", os.getenv("DATABASE_URL", ""))

    async def get_openai_key(self) -> str:
        """Get OPENAI_API_KEY from Dapr secrets."""
        secrets = await self.get_secret("todo-secrets")
        return secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY", ""))

    async def get_auth_secret(self) -> str:
        """Get BETTER_AUTH_SECRET from Dapr secrets."""
        secrets = await self.get_secret("todo-secrets")
        return secrets.get("BETTER_AUTH_SECRET", os.getenv("BETTER_AUTH_SECRET", ""))


class DaprJobsClient:
    """
    Dapr Jobs API client.
    
    Building Block 4.5: Jobs/Scheduling
    Schedule jobs for future execution (reminders, recurring tasks).
    """

    def __init__(self):
        self.dapr_port = int(os.getenv("DAPR_HTTP_PORT", "3500"))
        self.base_url = f"http://localhost:{self.dapr_port}/v1.0-alpha1"

    async def schedule_job(
        self,
        job_name: str,
        schedule: str,
        data: dict[str, Any],
        callback_url: str = "/jobs/callback",
    ) -> bool:
        """
        Schedule a job using Dapr Jobs API.
        
        Uses: POST /v1.0-alpha1/jobs/{job-name}
        
        Args:
            job_name: Unique identifier for the job
            schedule: Cron expression or ISO 8601 duration
            data: Data to pass to the callback
            callback_url: Endpoint to call when job triggers
        """
        url = f"{self.base_url}/jobs/{job_name}"

        job_spec = {
            "schedule": schedule,
            "data": data,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    json=job_spec,
                    headers={"Content-Type": "application/json"},
                )
                return response.status_code in (200, 201, 204)
            except httpx.RequestError as e:
                print(f"[Dapr] Jobs API not available: {e}")
                return False

    async def schedule_reminder(
        self,
        task_id: int,
        user_id: str,
        title: str,
        remind_at: str,
    ) -> bool:
        """Schedule a reminder job for a task."""
        job_name = f"reminder-{task_id}-{user_id}"
        return await self.schedule_job(
            job_name=job_name,
            schedule=remind_at,  # ISO 8601 datetime
            data={
                "task_id": task_id,
                "user_id": user_id,
                "title": title,
                "type": "reminder",
            },
        )

    async def delete_job(self, job_name: str) -> bool:
        """Delete a scheduled job."""
        url = f"{self.base_url}/jobs/{job_name}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(url)
                return response.status_code in (200, 204)
            except httpx.RequestError:
                return False


# Global instances
service_client = DaprServiceClient()
secrets_client = DaprSecretsClient()
jobs_client = DaprJobsClient()
