import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app import service
from app.auth import get_current_user, create_token
from app.database import get_db
from app.models import TodoStatus, User
from app.schemas import (
    TodoCreate, TodoUpdate, TodoResponse, PaginatedResponse,
    UserCreate, UserResponse, LoginRequest, TokenResponse
)

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    return {"status": "ok"}


# -- Auth ------------------------------------------------------------------

@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, payload)


@router.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    u = service.authenticate_user(db, req.email, req.password)
    if not u:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token = create_token(u.id)
    return {"access_token": token, "token_type": "bearer", "user": u}


# -- Todos -----------------------------------------------------------------

@router.get("/todos", response_model=PaginatedResponse)
def list_todos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: TodoStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    items, total = service.get_todos(db, user.id, page=page, page_size=page_size, status=status)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(
    payload: TodoCreate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.create_todo(db, user.id, payload)


@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(
    todo_id: uuid.UUID, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.get_todo(db, user.id, todo_id)


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: uuid.UUID, 
    updates: TodoUpdate, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.update_todo(db, user.id, todo_id, updates)


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(
    todo_id: uuid.UUID, 
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    service.delete_todo(db, user.id, todo_id)
