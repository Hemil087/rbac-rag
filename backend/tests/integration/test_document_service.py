from app.db.database import SessionLocal
from app.services.document_service import get_user_accessible_documents


def test_service_returns_accessible_documents_for_acme_employee():
    db = SessionLocal()

    try:
        documents = get_user_accessible_documents(
            db=db,
            org_id=3,
            role_id=7,
        )

        filenames = [document.filename for document in documents]

        assert filenames == ["engineering_handbook.pdf"]

    finally:
        db.close()