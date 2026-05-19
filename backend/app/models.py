import enum
import uuid
from datetime import datetime, date

from sqlalchemy import String, Text, Date, Enum, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class TodoStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_status", "status"),
        Index("ix_todos_due_date", "due_date"),
        Index("ix_todos_user_id", "user_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus, name="todo_status", native_enum=False),
        default=TodoStatus.pending,
    )
    due_date: Mapped[date | None] = mapped_column(Date, default=None)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
