"""Database connection for Neon PostgreSQL.

Reference: @specs/database/schema.md
"""

import ssl
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config import get_settings

settings = get_settings()

# Process database URL - asyncpg handles SSL differently
database_url = settings.database_url

# Create async engine
engine_kwargs: dict = {"echo": False}

# Only add pool settings and SSL for PostgreSQL
if "postgresql" in database_url:
    # Remove sslmode from URL as asyncpg handles it via connect_args
    database_url = database_url.replace("?sslmode=require", "").replace("&sslmode=require", "")
    
    # Create SSL context for Neon
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    engine_kwargs.update({
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
        "connect_args": {"ssl": ssl_context},
    })

engine = create_async_engine(database_url, **engine_kwargs)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Initialize database and create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
