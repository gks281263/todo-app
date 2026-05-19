import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import service
from app.database import get_db
from app.models import TodoStatus
from app.schemas import TodoCreate, TodoUpdate, TodoResponse, PaginatedResponse

router = APIRouter(prefix="/api")


@router.get("/health")
def health_check():
    return {"status": "ok"}


# -- Todos -----------------------------------------------------------------

@router.get("/todos", response_model=PaginatedResponse)
def list_todos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: TodoStatus | None = None,
    db: Session = Depends(get_db),
):
    items, total = service.get_todos(db, page=page, page_size=page_size, status=status)
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(data: TodoCreate, db: Session = Depends(get_db)):
    return service.create_todo(db, data)


@router.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: uuid.UUID, db: Session = Depends(get_db)):
    return service.get_todo(db, todo_id)


@router.patch("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: uuid.UUID, data: TodoUpdate, db: Session = Depends(get_db)
):
    return service.update_todo(db, todo_id, data)


@router.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: uuid.UUID, db: Session = Depends(get_db)):
    service.delete_todo(db, todo_id)
