from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Role


def get_org_roles(db: Session, org_id: int):
    statement = (
        select(Role)
        .where(Role.org_id == org_id)
        .order_by(Role.created_at.desc())
    )
    return db.execute(statement).scalars().all()


def get_role_by_id(db: Session, role_id: int, org_id: int):
    statement = (
        select(Role)
        .where(Role.id == role_id, Role.org_id == org_id)
    )
    return db.execute(statement).scalar_one_or_none()


def create_role(db: Session, org_id: int, role_name: str):
    role = Role(org_id=org_id, role_name=role_name)
    db.add(role)
    db.flush()
    return role


def update_role(db: Session, role: Role, **kwargs):
    for key, value in kwargs.items():
        if value is not None:
            setattr(role, key, value)
    db.flush()
    return role


def delete_role(db: Session, role: Role):
    db.delete(role)
    db.flush()
