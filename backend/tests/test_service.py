import uuid
import pytest

from app import service
from app.schemas import TodoCreate, TodoUpdate
from app.exceptions import TodoNotFound


def test_create_and_fetch(db):
    todo = service.create_todo(db, TodoCreate(title="Write tests"))
    assert todo.title == "Write tests"
    assert todo.status.value == "pending"

    fetched = service.get_todo(db, todo.id)
    assert fetched.id == todo.id


def test_get_missing_raises(db):
    with pytest.raises(TodoNotFound):
        service.get_todo(db, uuid.uuid4())


def test_update(db):
    todo = service.create_todo(db, TodoCreate(title="Old"))
    updated = service.update_todo(db, todo.id, TodoUpdate(title="New"))
    assert updated.title == "New"


def test_update_missing_raises(db):
    with pytest.raises(TodoNotFound):
        service.update_todo(db, uuid.uuid4(), TodoUpdate(title="Nope"))


def test_delete(db):
    todo = service.create_todo(db, TodoCreate(title="Temporary"))
    service.delete_todo(db, todo.id)

    with pytest.raises(TodoNotFound):
        service.get_todo(db, todo.id)


def test_list_filtered(db):
    service.create_todo(db, TodoCreate(title="A"))
    service.create_todo(db, TodoCreate(title="B", status="completed"))

    items, total = service.get_todos(db, status="completed")
    assert total == 1
    assert items[0].title == "B"


def test_list_paginated(db):
    for i in range(3):
        service.create_todo(db, TodoCreate(title=f"T{i}"))

    items, total = service.get_todos(db, page=2, page_size=2)
    assert total == 3
    assert len(items) == 1
