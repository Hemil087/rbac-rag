from app.db.repositories.document_repository import (
    get_accessible_documents,
)


def test_acme_employee_can_access_engineering_handbook(
    db_session,
):

    documents = get_accessible_documents(
        db=db_session,
        org_id=1,
        role_id=3,
    )

    filenames = [
        document.filename
        for document in documents
    ]

    assert "engineering_handbook.pdf" in filenames


def test_acme_employee_cannot_access_globex_documents(
    db_session,
):

    documents = get_accessible_documents(
        db=db_session,
        org_id=1,
        role_id=3,
    )

    filenames = [
        document.filename
        for document in documents
    ]

    assert "globex_hr_policy.pdf" not in filenames


def test_globex_employee_can_access_globex_hr_policy(
    db_session,
):

    documents = get_accessible_documents(
        db=db_session,
        org_id=2,
        role_id=5,
    )

    filenames = [
        document.filename
        for document in documents
    ]

    assert "globex_hr_policy.pdf" in filenames