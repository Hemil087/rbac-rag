from datetime import datetime
from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    role_name: str = Field(min_length=1, max_length=255)


class RoleUpdate(BaseModel):
    role_name: str | None = Field(None, min_length=1, max_length=255)


class RoleOut(BaseModel):
    id: int
    org_id: int
    role_name: str
    created_at: datetime

    model_config = {"from_attributes": True}
