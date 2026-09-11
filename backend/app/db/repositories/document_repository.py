from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentPermission


def get_accessible_documents(
    db: Session,
    org_id: int,
    role_id: int,
):
    statement = (
        select(Document)
        .join(
            DocumentPermission,
            (
                (Document.id == DocumentPermission.doc_id)
                & (Document.org_id == DocumentPermission.org_id)
            ),
        )
        .where(
            DocumentPermission.role_id == role_id,
            DocumentPermission.org_id == org_id,
        )
    )

    result = db.execute(statement)

    return result.scalars().all()