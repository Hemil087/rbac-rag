from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    role_id: int


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=6)
    role_id: int | None = None


class UserOut(BaseModel):
    id: int
    org_id: int
    role_id: int
    email: str
    created_at: datetime
    role_name: str | None = None

    model_config = {"from_attributes": True}
