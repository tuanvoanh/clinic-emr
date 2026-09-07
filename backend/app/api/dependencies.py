from typing import Generator
from app.core.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency func: Provides a Database Session for each API request.
    Automatically closes the session after the request is completed or if an error occurs.
    
    Yields:
        Session: SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
