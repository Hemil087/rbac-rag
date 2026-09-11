from app.db.database import SessionLocal
from app.db.repositories.document_repository import get_accessible_documents


def test_acme_employee_can_access_only_allowed_documents():
    db = SessionLocal()

    try:
        documents = get_accessible_documents(
            db=db,
            org_id=3,
            role_id=7,
        )

        filenames = [document.filename for document in documents]

        assert filenames == ["engineering_handbook.pdf"]

    finally:
        db.close()


def test_acme_employee_cannot_access_globex_documents():
    db = SessionLocal()

    try:
        documents = get_accessible_documents(
            db=db,
            org_id=4,
            role_id=7,
        )

        assert documents == []

    finally:
        db.close()


def test_globex_employee_can_access_only_allowed_documents():
    db = SessionLocal()

    try:
        documents = get_accessible_documents(
            db=db,
            org_id=4,
            role_id=9,
        )

        filenames = [document.filename for document in documents]

        assert filenames == ["globex_hr_policy.pdf"]

    finally:
        db.close()