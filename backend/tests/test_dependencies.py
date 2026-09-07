from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from jose import JWTError

from app.api import dependencies
from app.core.exceptions import AppException, ErrorCode


def test_get_current_user_prefers_bearer_token(monkeypatch):
    db = MagicMock()
    user = SimpleNamespace(id=12)
    decode = MagicMock(return_value={"sub": "12"})
    get_user = MagicMock(return_value=user)
    monkeypatch.setattr(dependencies.jwt, "decode", decode)
    monkeypatch.setattr(dependencies.user_repo, "get", get_user)
    bearer = HTTPAuthorizationCredentials(scheme="Bearer", credentials="bearer-token")

    result = dependencies.get_current_user(
        db=db, oauth_token="oauth-token", bearer_token=bearer
    )

    assert result is user
    decode.assert_called_once_with(
        "bearer-token",
        dependencies.settings.SECRET_KEY,
        algorithms=[dependencies.settings.ALGORITHM],
    )
    get_user.assert_called_once_with(db, user_id=12)


def test_get_current_user_requires_token():
    with pytest.raises(AppException) as exc_info:
        dependencies.get_current_user(
            db=MagicMock(), oauth_token=None, bearer_token=None
        )

    assert exc_info.value.error_code == ErrorCode.UNAUTHORIZED.code
    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_invalid_token(monkeypatch):
    monkeypatch.setattr(
        dependencies.jwt, "decode", MagicMock(side_effect=JWTError("invalid"))
    )

    with pytest.raises(AppException) as exc_info:
        dependencies.get_current_user(
            db=MagicMock(), oauth_token="bad-token", bearer_token=None
        )

    assert exc_info.value.error_code == ErrorCode.UNAUTHORIZED.code
    assert exc_info.value.message == "Could not validate credentials"


def test_get_current_user_rejects_unknown_user(monkeypatch):
    monkeypatch.setattr(
        dependencies.jwt, "decode", MagicMock(return_value={"sub": "99"})
    )
    monkeypatch.setattr(dependencies.user_repo, "get", MagicMock(return_value=None))

    with pytest.raises(AppException) as exc_info:
        dependencies.get_current_user(
            db=MagicMock(), oauth_token="valid-token", bearer_token=None
        )

    assert exc_info.value.error_code == ErrorCode.USER_NOT_FOUND.code
    assert exc_info.value.status_code == 404
