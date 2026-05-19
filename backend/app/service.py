import logging
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.exceptions import TodoNotFound
from app.models import Todo, TodoStatus
from app.schemas import TodoCreate, TodoUpdate

log = logging.getLogger(__name__)


def get_todos(db: Session, *, page=1, page_size=20, status: TodoStatus | None = None):
    q = select(Todo)
    if status:
        q = q.where(Todo.status == status)

    total = db.scalar(select(func.count()).select_from(q.subquery()))
    items = db.scalars(
        q.order_by(Todo.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return items, total


def get_todo(db: Session, todo_id: uuid.UUID) -> Todo:
    todo = db.get(Todo, todo_id)
    if not todo:
        raise TodoNotFound(todo_id)
    return todo


def create_todo(db: Session, data: TodoCreate) -> Todo:
    todo = Todo(**data.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    log.info("created todo %s", todo.id)
    return todo


def update_todo(db: Session, todo_id: uuid.UUID, data: TodoUpdate):
    todo = get_todo(db, todo_id)

    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(todo, k, v)

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: uuid.UUID):
    todo = get_todo(db, todo_id)
    db.delete(todo)
    db.commit()
