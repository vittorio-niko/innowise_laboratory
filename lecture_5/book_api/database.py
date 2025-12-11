"""
DB management module.
Handles DB setup, session creation and connection management.
"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator


DATABASE_URL = "sqlite:///./book_collection.db"

# Base class for models
Base = declarative_base()

# DB engine initialization
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Connect SQLite and FastAPI
    echo=False,
    pool_pre_ping=True,  # Check connection before interaction
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """
    Get DB session.

    Yields:
        Session: SQLAlchemy Session to work with DB

    Guarantees valid DB closure.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_database():
    """
    Create all tables in DB.
    """
    Base.metadata.create_all(bind=engine)


def check_database_connection() -> bool:
    """
    Checks database connection.

    Returns:
        bool: True (connection is successful,
        False (connection failure)
    """
    from sqlalchemy import text
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False