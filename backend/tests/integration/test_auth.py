from app.core.security import decode_access_token
from app.services.auth_service import authenticate_user


def test_authenticate_acme_employee(db_session):

    user = authenticate_user(
        db=db_session,
        email="employee@acme.com",
        password="employee123",
    )

    assert user is not None
    assert user.email == "employee@acme.com"
    assert user.org_id == 1
    assert user.role_id == 3


def test_authenticate_with_wrong_password(db_session):

    user = authenticate_user(
        db=db_session,
        email="employee@acme.com",
        password="wrong-password",
    )

    assert user is None


def test_authenticate_unknown_email(db_session):

    user = authenticate_user(
        db=db_session,
        email="unknown@acme.com",
        password="employee123",
    )

    assert user is None


def test_authenticate_unknown_domain(db_session):

    user = authenticate_user(
        db=db_session,
        email="employee@unknown.com",
        password="employee123",
    )

    assert user is None


from app.core.security import (
    create_access_token,
    decode_access_token,
)


def test_access_token_contains_user_context():

    token = create_access_token(
        user_id=3,
        org_id=1,
        role_id=3,
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "3"
    assert payload["org_id"] == 1
    assert payload["role_id"] == 3
    assert "exp" in payload