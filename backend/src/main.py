"""FastAPI application entry point.

Reference: @backend/CLAUDE.md
"""

import uvicorn
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_settings
from src.database import init_db
from src.routes import tasks, chat, dapr_events

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan - initialize database on startup."""
    print("🚀 Starting Todo Evolution API...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database ready!")
    print("🤖 AI Chatbot enabled (Phase III)")
    print("📡 Dapr Event-Driven enabled (Phase V)")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(chat.router)
app.include_router(dapr_events.router)  # Phase V: Dapr events


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint - API info."""
    return {
        "name": settings.api_title,
        "version": settings.api_version,
        "docs": "/docs",
        "phase": "V - Event-Driven",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "phase": "V"}


def run_server() -> None:
    """Run the server with uvicorn."""
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=settings.api_port,
        reload=True,
    )


if __name__ == "__main__":
    run_server()
