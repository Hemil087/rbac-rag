from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import require_admin
from app.schemas.auth import CurrentUser
from app.schemas.roles import RoleCreate, RoleUpdate, RoleOut
from app.db.repositories.role_repository import (
    get_org_roles, get_role_by_id, create_role,
    update_role, delete_role,
)

router = APIRouter(
    prefix="/api/v1/roles",
    tags=["roles"],
)


@router.get("/", response_model=list[RoleOut])
def list_roles(
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return get_org_roles(db=db, org_id=current_user.org_id)


@router.get("/{role_id}", response_model=RoleOut)
def get_role(
    role_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    role = get_role_by_id(db=db, role_id=role_id, org_id=current_user.org_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_new_role(
    request: RoleCreate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    try:
        role = create_role(
            db=db,
            org_id=current_user.org_id,
            role_name=request.role_name,
        )
        db.commit()
        db.refresh(role)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Role name already exists")
    return role


@router.patch("/{role_id}", response_model=RoleOut)
def patch_role(
    role_id: int,
    request: RoleUpdate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    role = get_role_by_id(db=db, role_id=role_id, org_id=current_user.org_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    updates = request.model_dump(exclude_unset=True)
    try:
        role = update_role(db=db, role=role, **updates)
        db.commit()
        db.refresh(role)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Role name already exists")
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_role(
    role_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    role = get_role_by_id(db=db, role_id=role_id, org_id=current_user.org_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    try:
        delete_role(db=db, role=role)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cannot delete role: it is assigned to users or document permissions",
        )
