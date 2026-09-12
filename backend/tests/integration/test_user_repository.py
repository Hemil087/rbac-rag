from app.db.repositories.user_repository import (
    get_user_by_org_and_email,
)


def test_get_acme_employee(
    db_session,
):

    user = get_user_by_org_and_email(
        db=db_session,
        org_id=1,
        email="employee@acme.com",
    )

    assert user is not None
    assert user.email == "employee@acme.com"
    assert user.org_id == 1
    assert user.role_id == 3


def test_unknown_user(
    db_session,
):

    user = get_user_by_org_and_email(
        db=db_session,
        org_id=1,
        email="doesnotexist@acme.com",
    )

    assert user is None