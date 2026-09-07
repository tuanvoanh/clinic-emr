from datetime import timedelta
from typing import cast

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.exceptions import AppException, ErrorCode
from app.repositories.user import user_repo
from app.schemas.token import Token
from app.schemas.user import UserResponse, UserCreate

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = user_repo.get_by_email(db, email=form_data.username)
    if not user or not verify_password(
        form_data.password, cast(str, user.hashed_password)
    ):
        raise AppException(
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=400,
            message="Incorrect email or password"
        )
    elif not user.is_active:
        raise AppException(
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=400,
            message="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/setup", response_model=UserResponse)
def setup_first_user(db: Session = Depends(get_db)):
    """
    Setup the first superuser. If a user already exists, this endpoint fails.
    """
    from app.models.user import User
    user = db.query(User).first()
    if user:
        raise AppException(
            error_code=ErrorCode.VALIDATION_ERROR,
            status_code=400,
            message="Setup has already been completed."
        )
    user_in = UserCreate(
        email=settings.FIRST_SUPERUSER_EMAIL,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        full_name=settings.FIRST_SUPERUSER_FULL_NAME,
        is_superuser=True
    )
    user = user_repo.create(db, obj_in=user_in)
    return user
