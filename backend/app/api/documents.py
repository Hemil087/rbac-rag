from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth import get_db
from app.api.dependencies import get_current_user
from app.services.document_service import get_user_accessible_documents
from app.schemas.auth import CurrentUser

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["documents"],
)


@router.get("/")
def get_documents(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    documents = get_user_accessible_documents(
        db=db,
        org_id=current_user.org_id,
        role_id=current_user.role_id,
    )

    return [
        {
            "id": document.id,
            "filename": document.filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
        }
        for document in documents
    ]