from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.api.endpoints import auth
from app.core.exceptions import AppException, ErrorCode


def test_login_returns_access_token(monkeypatch):
    db = MagicMock()
    user = SimpleNamespace(id=7, hashed_password="hash", is_active=True)
    form = SimpleNamespace(username="doctor@example.com", password="secret")
    monkeypatch.setattr(auth.user_repo, "get_by_email", MagicMock(return_value=user))
    monkeypatch.setattr(auth, "verify_password", MagicMock(return_value=True))
    create_token = MagicMock(return_value="signed-token")
    monkeypatch.setattr(auth, "create_access_token", create_token)

    result = auth.login_access_token(db=db, form_data=form)

    assert result.access_token == "signed-token"
    assert result.token_type == "bearer"
    auth.user_repo.get_by_email.assert_called_once_with(db, email=form.username)
    create_token.assert_called_once()


@pytest.mark.parametrize(
    ("user", "password_valid", "message"),
    [
        (None, False, "Incorrect email or password"),
        (SimpleNamespace(hashed_password="hash", is_active=True), False, "Incorrect email or password"),
        (SimpleNamespace(hashed_password="hash", is_active=False), True, "Inactive user"),
    ],
)
def test_login_rejects_invalid_credentials_or_inactive_user(
    monkeypatch, user, password_valid, message
):
    monkeypatch.setattr(auth.user_repo, "get_by_email", MagicMock(return_value=user))
    monkeypatch.setattr(auth, "verify_password", MagicMock(return_value=password_valid))
    form = SimpleNamespace(username="doctor@example.com", password="wrong")

    with pytest.raises(AppException) as exc_info:
        auth.login_access_token(db=MagicMock(), form_data=form)

    assert exc_info.value.error_code == ErrorCode.UNAUTHORIZED.code
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == message


def test_setup_first_user_creates_configured_superuser(monkeypatch):
    db = MagicMock()
    db.query.return_value.first.return_value = None
    created_user = SimpleNamespace(id=1, email="admin@example.com")
    create = MagicMock(return_value=created_user)
    monkeypatch.setattr(auth.user_repo, "create", create)

    result = auth.setup_first_user(db=db)

    assert result is created_user
    user_in = create.call_args.kwargs["obj_in"]
    assert user_in.email == auth.settings.FIRST_SUPERUSER_EMAIL
    assert user_in.is_superuser is True


def test_setup_first_user_rejects_repeated_setup():
    db = MagicMock()
    db.query.return_value.first.return_value = SimpleNamespace(id=1)

    with pytest.raises(AppException) as exc_info:
        auth.setup_first_user(db=db)

    assert exc_info.value.error_code == ErrorCode.VALIDATION_ERROR.code
    assert exc_info.value.status_code == 400
