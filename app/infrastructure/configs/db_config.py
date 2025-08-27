from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.infrastructure.configs.app_config import app_settings

# --- Database URLs ---
SYNC_DATABASE_URL = (
    f"mysql+pymysql://{app_settings.database_user}:{app_settings.database_password}"
    f"@{app_settings.database_host}:{app_settings.database_port}/"
    f"{app_settings.database_name}"
)

ASYNC_DATABASE_URL = (
    f"mysql+aiomysql://{app_settings.database_user}:{app_settings.database_password}"
    f"@{app_settings.database_host}:{app_settings.database_port}/"
    f"{app_settings.database_name}"
)

# --- Sync engine (for Alembic and scripts) ---
sync_engine = create_engine(
    SYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)

# --- Async engine (for FastAPI runtime) ---
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# --- Declarative base ---
Base = declarative_base()


# --- Dependencies for FastAPI ---
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_db():
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
