from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Conversation


def create_conversation(
    db: Session,
    user_id: int,
    org_id: int,
    title: str,
):
    conversation = Conversation(
        user_id=user_id,
        org_id=org_id,
        title=title,
    )
    db.add(conversation)
    db.flush()
    return conversation


def get_user_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
    org_id: int,
):
    statement = (
        select(Conversation)
        .where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
            Conversation.org_id == org_id,
        )
    )
    return db.execute(statement).scalar_one_or_none()


def get_user_conversations(
    db: Session,
    user_id: int,
    org_id: int,
):
    statement = (
        select(Conversation)
        .where(
            Conversation.user_id == user_id,
            Conversation.org_id == org_id,
        )
        .order_by(Conversation.updated_at.desc())
    )
    return db.execute(statement).scalars().all()


def update_conversation(db: Session, conversation: Conversation, **kwargs):
    for key, value in kwargs.items():
        if value is not None:
            setattr(conversation, key, value)
    db.flush()
    return conversation


def delete_conversation(db: Session, conversation: Conversation):
    db.delete(conversation)
    db.flush()
