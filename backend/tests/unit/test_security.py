from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_can_be_verified():
    password = "test-password-123"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)


def test_wrong_password_fails_verification():
    password = "test-password-123"

    hashed_password = hash_password(password)

    assert not verify_password(
        "wrong-password",
        hashed_password,
    )


def test_access_token_contains_user_context():
    token = create_access_token(
        user_id=5,
        org_id=3,
        role_id=7,
    )

    payload = decode_access_token(token)

    assert payload["sub"] == "5"
    assert payload["org_id"] == 3
    assert payload["role_id"] == 7
    assert "exp" in payload