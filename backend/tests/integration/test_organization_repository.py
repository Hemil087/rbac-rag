from app.db.database import SessionLocal
from app.db.repositories.organization_repository import (
    get_organization_by_email_domain,
)


def test_find_acme_organization_by_email_domain():
    db = SessionLocal()

    try:
        organization = get_organization_by_email_domain(
            db=db,
            email_domain="acme.com",
        )

        assert organization is not None
        assert organization.id == 3
        assert organization.name == "Acme Corporation"

    finally:
        db.close()


def test_unknown_email_domain_returns_none():
    db = SessionLocal()

    try:
        organization = get_organization_by_email_domain(
            db=db,
            email_domain="unknown.com",
        )

        assert organization is None

    finally:
        db.close()