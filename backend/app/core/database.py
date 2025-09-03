"""Enhanced database connection and session management for the application core."""

from contextlib import contextmanager
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import settings


# Create database engine with enhanced configuration
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    connect_args={
        "check_same_thread": False,
        "timeout": 20
    } if "sqlite" in settings.database_url else {},
    poolclass=StaticPool if "sqlite" in settings.database_url else None,
    pool_pre_ping=True,
    pool_recycle=3600
)


def create_db_and_tables():
    """Create database and all tables with proper error handling."""
    try:
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        raise


def get_session() -> Generator[Session, None, None]:
    """Get database session with proper cleanup."""
    with Session(engine) as session:
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """Context manager for database sessions."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database():
    """Initialize database with all required tables."""
    create_db_and_tables()


def check_database_connection() -> bool:
    """Check if database connection is working."""
    try:
        with Session(engine) as session:
            session.exec("SELECT 1")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
