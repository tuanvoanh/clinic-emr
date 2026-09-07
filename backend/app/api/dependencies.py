from typing import Generator
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.config import settings
from app.core.exceptions import AppException, ErrorCode
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.token import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login/access-token")

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

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise AppException(
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=401,
            message="Could not validate credentials"
        )
    user = user_repo.get(db, user_id=int(token_data.sub))
    if not user:
        raise AppException(
            error_code=ErrorCode.USER_NOT_FOUND,
            status_code=404,
            message="User not found"
        )
    return user
