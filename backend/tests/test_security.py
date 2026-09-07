from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core import security


def decode_token(token):
    return jwt.decode(
        token,
        security.settings.SECRET_KEY,
        algorithms=[security.settings.ALGORITHM],
    )


def test_create_access_token_uses_custom_expiry():
    before = datetime.now(timezone.utc)

    payload = decode_token(
        security.create_access_token("doctor-1", expires_delta=timedelta(minutes=5))
    )

    expires_at = datetime.fromtimestamp(payload["exp"], timezone.utc)
    assert payload["sub"] == "doctor-1"
    assert before + timedelta(minutes=4, seconds=55) <= expires_at
    assert expires_at <= before + timedelta(minutes=5, seconds=5)


def test_create_access_token_uses_default_expiry():
    before = datetime.now(timezone.utc)

    payload = decode_token(security.create_access_token(42))

    expires_at = datetime.fromtimestamp(payload["exp"], timezone.utc)
    expected = timedelta(minutes=security.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    assert payload["sub"] == "42"
    assert before + expected - timedelta(seconds=5) <= expires_at
    assert expires_at <= before + expected + timedelta(seconds=5)


def test_password_hash_can_be_verified():
    password_hash = security.get_password_hash("strong-password")

    assert password_hash != "strong-password"
    assert security.verify_password("strong-password", password_hash) is True
    assert security.verify_password("wrong-password", password_hash) is False
