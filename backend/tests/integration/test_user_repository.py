from app.db.database import SessionLocal
from app.db.repositories.user_repository import get_user_by_org_and_email


def test_find_acme_employee():
    db = SessionLocal()

    try:
        user = get_user_by_org_and_email(
            db=db,
            org_id=3,
            email="employee@acme.com",
        )

        assert user is not None
        assert user.id == 5
        assert user.org_id == 3
        assert user.role_id == 7

    finally:
        db.close()


def test_same_email_in_wrong_organization_returns_none():
    db = SessionLocal()

    try:
        user = get_user_by_org_and_email(
            db=db,
            org_id=4,
            email="employee@acme.com",
        )

        assert user is None

    finally:
        db.close()