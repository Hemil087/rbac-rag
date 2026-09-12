import pytest
from fastapi import HTTPException

from app.api.dependencies import get_current_user
from app.core.security import create_access_token


def test_get_current_user_from_valid_token():

    token = create_access_token(
        user_id=3,
        org_id=1,
        role_id=3,
    )

    current_user = get_current_user(token)

    assert current_user.user_id == 3
    assert current_user.org_id == 1
    assert current_user.role_id == 3


def test_get_current_user_rejects_invalid_token():

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(
            "this-is-not-a-valid-token"
        )

    assert exc_info.value.status_code == 401


def test_get_current_user_rejects_incomplete_token():

    from jose import jwt

    import os

    secret = os.getenv("JWT_SECRET_KEY")
    algorithm = os.getenv(
        "JWT_ALGORITHM",
        "HS256",
    )

    token = jwt.encode(
        {
            "sub": "3",
            "org_id": 1,
        },
        secret,
        algorithm=algorithm,
    )

    with pytest.raises(HTTPException) as exc_info:

        get_current_user(token)

    assert exc_info.value.status_code == 401