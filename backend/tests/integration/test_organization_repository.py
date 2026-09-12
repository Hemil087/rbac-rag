from app.db.repositories.organization_repository import (
    get_organization_by_email_domain,
)


def test_get_acme_organization(
    db_session,
):

    organization = (
        get_organization_by_email_domain(
            db=db_session,
            email_domain="acme.com",
        )
    )

    assert organization is not None
    assert organization.id == 1
    assert organization.name == "Acme Corporation"
    assert organization.email_domain == "acme.com"


def test_get_unknown_organization(
    db_session,
):

    organization = (
        get_organization_by_email_domain(
            db=db_session,
            email_domain="unknown.com",
        )
    )

    assert organization is None