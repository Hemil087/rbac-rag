from datetime import datetime
from pydantic import BaseModel, Field


class DocumentCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    storage_path: str = Field(min_length=1, max_length=500)
    file_type: str = Field(min_length=1, max_length=100)
    file_size: int = Field(ge=0)


class DocumentUpdate(BaseModel):
    filename: str | None = Field(None, min_length=1, max_length=255)
    storage_path: str | None = Field(None, min_length=1, max_length=500)
    file_type: str | None = Field(None, min_length=1, max_length=100)
    file_size: int | None = Field(None, ge=0)


class DocumentOut(BaseModel):
    id: int
    org_id: int
    filename: str
    storage_path: str
    file_type: str
    file_size: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PermissionCreate(BaseModel):
    role_id: int


class PermissionOut(BaseModel):
    doc_id: int
    role_id: int
    org_id: int
    role_name: str | None = None

    model_config = {"from_attributes": True}
