from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import SessionLocal
from app.schemas.auth import LoginRequest, TokenResponse, CurrentUser
from app.services.auth_service import authenticate_user
from app.api.dependencies import get_current_user


router = APIRouter(
    prefix = '/api/v1/auth',
    tags = ["authentication"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login",response_model = TokenResponse)
def login(
    request : LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db = db,
        email = request.email,
        password=request.password,
    )
    if user is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or Password",
        )
    access_token = create_access_token(
        user_id = user.id,
        org_id=user.org_id,
        role_id = user.role_id,
    )
    return TokenResponse(
        access_token = access_token,
        token_type = "bearer",
    )


@router.get("/me")
def get_me(
    current_user: CurrentUser = Depends(get_current_user),
):
    return current_user