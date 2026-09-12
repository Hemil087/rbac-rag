from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Organization


def get_organization_by_email_domain(
    db: Session,
    email_domain: str,
):
    statement = (
        select(Organization)
        .where(Organization.email_domain == email_domain)
    )

    result = db.execute(statement)

    return result.scalar_one_or_none()