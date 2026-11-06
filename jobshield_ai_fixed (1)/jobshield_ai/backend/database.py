"""
Database connection and session management for JobShield AI.

Supports:
  * SQLite  (local development, zero setup)
  * PostgreSQL / MySQL (production, e.g. Neon, Supabase, PlanetScale, Railway)

Vercel note: the Vercel filesystem is READ-ONLY except /tmp, and /tmp is wiped on
every cold start. So on Vercel a SQLite file is placed in /tmp (data is temporary).
For persistent data on Vercel, set DATABASE_URL to a hosted Postgres/MySQL database.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.config import DATABASE_URL

logger = logging.getLogger("jobshield.database")
logging.basicConfig(level=logging.INFO)

Base = declarative_base()

IS_VERCEL = bool(os.getenv("VERCEL"))
SQLITE_FALLBACK_URL = "sqlite:////tmp/jobshield.db" if IS_VERCEL else "sqlite:///./jobshield.db"


def _normalize_url(url: str) -> str:
    """Fix URL styles that SQLAlchemy rejects (Heroku/Neon/Supabase give 'postgres://')."""
    url = (url or "").strip().strip('"').strip("'")
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"):]
    if url.startswith("sqlite:///./") and IS_VERCEL:
        # Relative sqlite path is read-only on Vercel -> use /tmp
        url = "sqlite:////tmp/" + url[len("sqlite:///./"):]
    return url


def _sqlite_engine(url: str):
    return create_engine(url, connect_args={"check_same_thread": False})


def get_database_engine():
    target_url = _normalize_url(DATABASE_URL) or SQLITE_FALLBACK_URL

    if target_url.startswith("sqlite"):
        return _sqlite_engine(target_url)

    # Hosted database (PostgreSQL / MySQL)
    try:
        engine = create_engine(target_url, pool_pre_ping=True)
        with engine.connect():
            pass
        logger.info("Successfully connected to %s database.", engine.name)
        return engine
    except Exception as e:
        logger.warning(
            "Could not connect to configured database (%s). "
            "Falling back to local SQLite (%s).", e, SQLITE_FALLBACK_URL
        )
        return _sqlite_engine(SQLITE_FALLBACK_URL)


engine = get_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI Dependency for database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
