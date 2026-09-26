from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import require_admin
from app.core.security import hash_password
from app.schemas.auth import CurrentUser
from app.schemas.users import UserCreate, UserUpdate, UserOut
from app.db.repositories.user_repository import (
    get_org_users, get_user_by_id, create_user,
    update_user, delete_user, get_user_by_org_and_email,
)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
)


@router.get("/", response_model=list[UserOut])
def list_users(
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    rows = get_org_users(db=db, org_id=current_user.org_id)
    return [
        UserOut(
            id=user.id,
            org_id=user.org_id,
            role_id=user.role_id,
            email=user.email,
            created_at=user.created_at,
            role_name=role_name,
        )
        for user, role_name in rows
    ]


@router.get("/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    row = get_user_by_id(db=db, user_id=user_id, org_id=current_user.org_id)
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user, role_name = row
    return UserOut(
        id=user.id,
        org_id=user.org_id,
        role_id=user.role_id,
        email=user.email,
        created_at=user.created_at,
        role_name=role_name,
    )


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_new_user(
    request: UserCreate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    existing = get_user_by_org_and_email(
        db=db, org_id=current_user.org_id, email=request.email,
    )
    if existing is not None:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    user = create_user(
        db=db,
        org_id=current_user.org_id,
        email=request.email,
        hashed_password=hash_password(request.password),
        role_id=request.role_id,
    )
    db.commit()
    db.refresh(user)
    return UserOut(
        id=user.id,
        org_id=user.org_id,
        role_id=user.role_id,
        email=user.email,
        created_at=user.created_at,
        role_name=None,
    )


@router.patch("/{user_id}", response_model=UserOut)
def patch_user(
    user_id: int,
    request: UserUpdate,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    row = get_user_by_id(db=db, user_id=user_id, org_id=current_user.org_id)
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user, _ = row

    updates = request.model_dump(exclude_unset=True)
    if "password" in updates:
        updates["hashed_password"] = hash_password(updates.pop("password"))
    user = update_user(db=db, user=user, **updates)
    db.commit()
    db.refresh(user)

    row2 = get_user_by_id(db=db, user_id=user_id, org_id=current_user.org_id)
    user2, role_name = row2
    return UserOut(
        id=user2.id,
        org_id=user2.org_id,
        role_id=user2.role_id,
        email=user2.email,
        created_at=user2.created_at,
        role_name=role_name,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    current_user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if user_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")

    row = get_user_by_id(db=db, user_id=user_id, org_id=current_user.org_id)
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user, _ = row
    delete_user(db=db, user=user)
    db.commit()
