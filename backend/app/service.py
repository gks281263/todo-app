import logging
import uuid

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.exceptions import TodoNotFound
from app.models import Todo, TodoStatus, User
from app.schemas import TodoCreate, TodoUpdate, UserCreate
from app.auth import hash_pw, verify_pw

log = logging.getLogger(__name__)


def create_user(db: Session, data: UserCreate) -> User:
    if db.scalar(select(User).where(User.email == data.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    u = User(email=data.email, password_hash=hash_pw(data.password))
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


def authenticate_user(db: Session, email: str, password: str):
    u = db.scalar(select(User).where(User.email == email))
    if not u or not verify_pw(password, u.password_hash):
        return None
    return u


def get_todos(db: Session, uid: uuid.UUID, page=1, page_size=20, status: TodoStatus | None = None):
    query = select(Todo).where(Todo.user_id == uid)
    if status:
        query = query.where(Todo.status == status)

    total_count = db.scalar(select(func.count()).select_from(query.subquery()))
    
    results = db.scalars(
        query.order_by(Todo.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return results, total_count


def get_todo(db: Session, uid: uuid.UUID, todo_id: uuid.UUID) -> Todo:
    t = db.scalar(select(Todo).where(Todo.id == todo_id, Todo.user_id == uid))
    if not t:
        raise TodoNotFound(todo_id)
    return t


def create_todo(db: Session, uid: uuid.UUID, payload: TodoCreate) -> Todo:
    new_todo = Todo(**payload.model_dump(), user_id=uid)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    log.info(f"User {uid} created todo {new_todo.id}")
    return new_todo


def update_todo(db: Session, uid: uuid.UUID, todo_id: uuid.UUID, updates: TodoUpdate):
    t = get_todo(db, uid, todo_id)
    
    # only update fields that were actually passed
    for field, val in updates.model_dump(exclude_unset=True).items():
        setattr(t, field, val)

    db.commit()
    db.refresh(t)
    return t


def delete_todo(db: Session, uid: uuid.UUID, todo_id: uuid.UUID):
    t = get_todo(db, uid, todo_id)
    db.delete(t)
    db.commit()
