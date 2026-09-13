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