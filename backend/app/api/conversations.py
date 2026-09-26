from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.api.dependencies import get_current_user
from app.schemas.auth import CurrentUser
from app.schemas.conversations import ConversationUpdate, ConversationOut, MessageOut
from app.db.repositories.conversation_repository import (
    get_user_conversations, get_user_conversation,
    update_conversation, delete_conversation,
)
from app.db.repositories.message_repository import get_conversation_messages

router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["conversations"],
)


@router.get("/", response_model=list[ConversationOut])
def list_conversations(
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_user_conversations(
        db=db,
        user_id=current_user.user_id,
        org_id=current_user.org_id,
    )


@router.get("/{conversation_id}", response_model=ConversationOut)
def get_conversation(
    conversation_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.user_id,
        org_id=current_user.org_id,
    )
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv


@router.patch("/{conversation_id}", response_model=ConversationOut)
def patch_conversation(
    conversation_id: int,
    request: ConversationUpdate,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.user_id,
        org_id=current_user.org_id,
    )
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    updates = request.model_dump(exclude_unset=True)
    conv = update_conversation(db=db, conversation=conv, **updates)
    db.commit()
    db.refresh(conv)
    return conv


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_conversation(
    conversation_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.user_id,
        org_id=current_user.org_id,
    )
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    delete_conversation(db=db, conversation=conv)
    db.commit()


@router.get("/{conversation_id}/messages", response_model=list[MessageOut])
def list_messages(
    conversation_id: int,
    current_user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conv = get_user_conversation(
        db=db,
        conversation_id=conversation_id,
        user_id=current_user.user_id,
        org_id=current_user.org_id,
    )
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return get_conversation_messages(db=db, conversation_id=conversation_id)
