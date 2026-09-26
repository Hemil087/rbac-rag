from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import get_current_user
from app.schemas.auth import CurrentUser
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat


router = APIRouter(
    prefix="/api/v1/chat",
    tags=["chat"],
)


@router.post("/", response_model=ChatResponse)
def chat_endpoint(
    request: ChatRequest,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        result = chat(
            db=db,
            user_id=current_user.user_id,
            org_id=current_user.org_id,
            role_id=current_user.role_id,
            question=request.question,
            conversation_id=request.conversation_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return ChatResponse(**result)