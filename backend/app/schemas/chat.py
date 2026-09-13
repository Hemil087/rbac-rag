from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    conversation_id: int | None = None


class ChatSource(BaseModel):
    document_id: int
    chunk_id: int
    chunk_index: int


class ChatResponse(BaseModel):
    conversation_id: int
    answer: str
    sources: list[ChatSource]