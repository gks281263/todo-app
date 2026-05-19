import uuid
from datetime import date, datetime

from pydantic import BaseModel, Field, field_validator

from app.models import TodoStatus


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    status: TodoStatus = TodoStatus.pending
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title cannot be blank")
        return v


class TodoUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = None
    status: TodoStatus | None = None
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def clean_title(cls, v):
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("title cannot be blank")
        return v


class TodoResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    title: str
    description: str | None
    status: TodoStatus
    due_date: date | None
    created_at: datetime
    updated_at: datetime


class PaginatedResponse(BaseModel):
    items: list[TodoResponse]
    total: int
    page: int
    page_size: int


class UserCreate(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator("email")
    @classmethod
    def clean_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v:
            raise ValueError("invalid email format")
        return v


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}
    
    id: uuid.UUID
    email: str
    created_at: datetime


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
