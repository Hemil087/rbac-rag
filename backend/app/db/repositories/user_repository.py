from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.models import User, Role


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


def get_org_users(db: Session, org_id: int):
    statement = (
        select(User, Role.role_name)
        .outerjoin(
            Role,
            (User.role_id == Role.id) & (User.org_id == Role.org_id),
        )
        .where(User.org_id == org_id)
        .order_by(User.created_at.desc())
    )
    return db.execute(statement).all()


def get_user_by_id(db: Session, user_id: int, org_id: int):
    statement = (
        select(User, Role.role_name)
        .outerjoin(
            Role,
            (User.role_id == Role.id) & (User.org_id == Role.org_id),
        )
        .where(User.id == user_id, User.org_id == org_id)
    )
    return db.execute(statement).first()


def create_user(db: Session, org_id: int, **kwargs):
    user = User(org_id=org_id, **kwargs)
    db.add(user)
    db.flush()
    return user


def update_user(db: Session, user: User, **kwargs):
    for key, value in kwargs.items():
        if value is not None:
            setattr(user, key, value)
    db.flush()
    return user


def delete_user(db: Session, user: User):
    db.delete(user)
    db.flush()
