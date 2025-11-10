import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..core.config import settings


def build_database_url() -> str:
    """Build a SQLAlchemy database URL.

    Priority:
    1) DATABASE_URL env (preferred on Railway). If present and missing driver, coerce to psycopg v3 driver.
    2) Compose from individual POSTGRES_* settings.
    """
    raw_url = os.getenv("DATABASE_URL") or ""
    if raw_url:
        # Normalize schemes to ensure psycopg v3 driver is used
        if raw_url.startswith("postgres://"):
            raw_url = "postgresql+psycopg://" + raw_url[len("postgres://") :]
        elif raw_url.startswith("postgresql://") and "+" not in raw_url.split("://", 1)[0]:
            raw_url = "postgresql+psycopg://" + raw_url[len("postgresql://") :]
        return raw_url

    return (
        f"postgresql+psycopg://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )


engine = create_engine(
    build_database_url(),
    pool_pre_ping=True,
    pool_size=int(os.getenv('DB_POOL_SIZE', 5)),
    max_overflow=int(os.getenv('DB_MAX_OVERFLOW', 10)),
    pool_timeout=int(os.getenv('DB_POOL_TIMEOUT', 30)),
    pool_recycle=int(os.getenv('DB_POOL_RECYCLE', 1800)),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
