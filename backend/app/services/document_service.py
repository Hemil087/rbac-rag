from sqlalchemy.orm import Session

from app.db.repositories.document_repository import get_accessible_documents


def get_user_accessible_documents(
    db: Session,
    org_id: int,
    role_id: int,
):
    return get_accessible_documents(
        db=db,
        org_id=org_id,
        role_id=role_id,
    )