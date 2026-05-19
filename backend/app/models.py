import enum
import uuid
from datetime import datetime, date

from sqlalchemy import String, Text, Date, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.database import Base


class TodoStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class Todo(Base):
    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_status", "status"),
        Index("ix_todos_due_date", "due_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus, name="todo_status", native_enum=False),
        default=TodoStatus.pending,
    )
    due_date: Mapped[date | None] = mapped_column(Date, default=None)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
