from datetime import datetime
from pydantic import BaseModel, Field


class ConversationUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)


class ConversationOut(BaseModel):
    id: int
    user_id: int
    org_id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageOut(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {"from_attributes": True}
