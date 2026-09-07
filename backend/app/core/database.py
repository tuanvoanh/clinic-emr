from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Initialize database connection engine
# `check_same_thread=False` is required for SQLite in FastAPI to prevent errors when multiple threads access the db
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Initialize SessionLocal factory to create independent database sessions for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
