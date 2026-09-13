from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Message


def create_message(
    db: Session,
    conversation_id: int,
    role: str,
    content: str,
):
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.flush()

    return message


def get_conversation_messages(
    db: Session,
    conversation_id: int,
):
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at, Message.id)
    )

    return db.execute(statement).scalars().all()