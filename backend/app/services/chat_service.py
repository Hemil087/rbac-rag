from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.repositories.conversation_repository import (
    create_conversation,
    get_user_conversation,
)
from app.db.repositories.message_repository import (
    create_message,
    get_conversation_messages,
)
from app.services.rag_service import generate_rag_answer


def chat(
    db: Session,
    user_id: int,
    org_id: int,
    role_id: int,
    question: str,
    conversation_id: int | None = None,
):
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    # 1. Get existing conversation or create a new one
    if conversation_id is None:
        conversation = create_conversation(
            db=db,
            user_id=user_id,
            org_id=org_id,
            title=question[:255],
        )
    else:
        conversation = get_user_conversation(
            db=db,
            conversation_id=conversation_id,
            user_id=user_id,
            org_id=org_id,
        )

        if conversation is None:
            raise ValueError("Conversation not found")

    # 2. Load previous conversation history
    previous_messages = get_conversation_messages(
        db=db,
        conversation_id=conversation.id,
    )

    conversation_history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in previous_messages
    ]

    # 3. Save current user message
    create_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=question,
    )

    # 4. Retrieve authorized context and generate answer
    answer, sources = generate_rag_answer(
        db=db,
        question=question,
        org_id=org_id,
        role_id=role_id,
        conversation_history=conversation_history,
    )

    # 5. Save assistant message
    create_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
    )

    # 6. Update conversation timestamp
    conversation.updated_at = datetime.now(timezone.utc)

    # 7. Commit the complete interaction
    db.commit()

    return {
        "conversation_id": conversation.id,
        "answer": answer,
        "sources": sources,
    }