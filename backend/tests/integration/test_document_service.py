from app.services.document_service import (
    get_user_accessible_documents,
)


def test_acme_employee_document_access(
    db_session,
):

    documents = get_user_accessible_documents(
        db=db_session,
        org_id=1,
        role_id=3,
    )

    filenames = [
        document.filename
        for document in documents
    ]

    assert "engineering_handbook.pdf" in filenames