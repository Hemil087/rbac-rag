from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import get_current_user, require_admin
from app.schemas.auth import CurrentUser
from app.schemas.documents import (
    DocumentCreate, DocumentUpdate, DocumentOut,
    PermissionCreate, PermissionOut,
)
from app.db.repositories.document_repository import (
    get_accessible_documents, get_org_documents, get_document_by_id,
    create_document, update_document, delete_document,
    get_document_permissions, add_document_permission, remove_document_permission,
)
from pathlib import Path
from uuid import uuid4
from app.services.ingestion_service import ingest_document

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["documents"],
)


@router.get("/", response_model=list[DocumentOut])
def list_documents(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    documents = get_accessible_documents(
        db=db,
        org_id=current_user.org_id,
        role_id=current_user.role_id,
    )
    return documents


@router.get("/all", response_model=list[DocumentOut])
def list_all_org_documents(
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return get_org_documents(db=db, org_id=current_user.org_id)

@router.post(
    "/upload",
    response_model=DocumentOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    # 1. Validate file type
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    original_filename = Path(file.filename).name

    if Path(original_filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    # 2. Create organization-specific storage directory
    storage_dir = Path("/app/storage") / str(current_user.org_id)
    storage_dir.mkdir(parents=True, exist_ok=True)

    # 3. Generate server-side filename
    stored_filename = f"{uuid4()}.pdf"
    storage_path = storage_dir / stored_filename

    # 4. Save uploaded file
    file_size = 0

    try:
        with storage_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)

                # 10 MB limit
                if file_size > 10 * 1024 * 1024:
                    raise HTTPException(
                        status_code=413,
                        detail="File size must not exceed 10 MB",
                    )

                output.write(chunk)

        # 5. Create document metadata
        document = create_document(
            db=db,
            org_id=current_user.org_id,
            filename=original_filename,
            storage_path=str(storage_path),
            file_type="pdf",
            file_size=file_size,
        )

        # 6. Extract → chunk → embed → store
        ingest_document(
            db=db,
            doc_id=document.id,
            file_path=str(storage_path),
        )

        # 7. Commit everything
        db.commit()
        db.refresh(document)

        return document

    except HTTPException:
        db.rollback()

        if storage_path.exists():
            storage_path.unlink()

        raise

    except Exception:
        db.rollback()

        if storage_path.exists():
            storage_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Failed to process document",
        )

    finally:
        await file.close()

@router.get("/{document_id}", response_model=DocumentOut)
def get_document(
    document_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.post("/", response_model=DocumentOut, status_code=status.HTTP_201_CREATED)
def create_doc(
    request: DocumentCreate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = create_document(
        db=db,
        org_id=current_user.org_id,
        filename=request.filename,
        storage_path=request.storage_path,
        file_type=request.file_type,
        file_size=request.file_size,
    )
    db.commit()
    db.refresh(doc)
    return doc


@router.patch("/{document_id}", response_model=DocumentOut)
def patch_document(
    document_id: int,
    request: DocumentUpdate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    updates = request.model_dump(exclude_unset=True)
    doc = update_document(db=db, document=doc, **updates)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_document(
    document_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    delete_document(db=db, document=doc)
    db.commit()


# --- Permissions ---

@router.get("/{document_id}/permissions")
def list_permissions(
    document_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    perms = get_document_permissions(db=db, doc_id=document_id, org_id=current_user.org_id)
    return [
        {
            "doc_id": perm.doc_id,
            "role_id": perm.role_id,
            "org_id": perm.org_id,
            "role_name": role_name,
        }
        for perm, role_name in perms
    ]


@router.post("/{document_id}/permissions", status_code=status.HTTP_201_CREATED)
def grant_permission(
    document_id: int,
    request: PermissionCreate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        perm = add_document_permission(
            db=db,
            doc_id=document_id,
            role_id=request.role_id,
            org_id=current_user.org_id,
        )
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Permission already exists or invalid role")

    return {"doc_id": perm.doc_id, "role_id": perm.role_id, "org_id": perm.org_id}


@router.delete("/{document_id}/permissions/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_permission(
    document_id: int,
    role_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    doc = get_document_by_id(db=db, doc_id=document_id, org_id=current_user.org_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="Document not found")

    removed = remove_document_permission(
        db=db, doc_id=document_id, role_id=role_id, org_id=current_user.org_id,
    )
    if removed == 0:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.commit()
