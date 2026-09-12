from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import User


def get_user_by_org_and_email(
    db: Session,
    org_id: int,
    email: str,
):
    statement = (
        select(User)
        .where(
            User.org_id == org_id,
            User.email == email,
        )
    )

    result = db.execute(statement)

    return result.scalar_one_or_none()