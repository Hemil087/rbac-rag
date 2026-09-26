from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentPermission, DocumentChunk, Role


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


def get_org_documents(db: Session, org_id: int):
    statement = (
        select(Document)
        .where(Document.org_id == org_id)
        .order_by(Document.created_at.desc())
    )
    return db.execute(statement).scalars().all()


def get_document_by_id(db: Session, doc_id: int, org_id: int):
    statement = (
        select(Document)
        .where(Document.id == doc_id, Document.org_id == org_id)
    )
    return db.execute(statement).scalar_one_or_none()


def create_document(db: Session, org_id: int, **kwargs):
    doc = Document(org_id=org_id, **kwargs)
    db.add(doc)
    db.flush()
    return doc


def update_document(db: Session, document: Document, **kwargs):
    for key, value in kwargs.items():
        if value is not None:
            setattr(document, key, value)
    db.flush()
    return document


def delete_document(db: Session, document: Document):
    db.delete(document)
    db.flush()


# --- Permissions ---

def get_document_permissions(db: Session, doc_id: int, org_id: int):
    statement = (
        select(DocumentPermission, Role.role_name)
        .join(
            Role,
            (
                (DocumentPermission.role_id == Role.id)
                & (DocumentPermission.org_id == Role.org_id)
            ),
        )
        .where(
            DocumentPermission.doc_id == doc_id,
            DocumentPermission.org_id == org_id,
        )
    )
    return db.execute(statement).all()


def add_document_permission(db: Session, doc_id: int, role_id: int, org_id: int):
    perm = DocumentPermission(
        doc_id=doc_id,
        role_id=role_id,
        org_id=org_id,
    )
    db.add(perm)
    db.flush()
    return perm


def remove_document_permission(db: Session, doc_id: int, role_id: int, org_id: int):
    statement = (
        delete(DocumentPermission)
        .where(
            DocumentPermission.doc_id == doc_id,
            DocumentPermission.role_id == role_id,
            DocumentPermission.org_id == org_id,
        )
    )
    result = db.execute(statement)
    db.flush()
    return result.rowcount
