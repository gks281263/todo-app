import uuid
import pytest

from app import service
from app.schemas import TodoCreate, TodoUpdate
from app.exceptions import TodoNotFound


def test_create_and_fetch(db, test_user):
    todo = service.create_todo(db, test_user.id, TodoCreate(title="Write tests"))
    assert todo.title == "Write tests"
    assert todo.status.value == "pending"

    fetched = service.get_todo(db, test_user.id, todo.id)
    assert fetched.id == todo.id


def test_get_missing_raises(db, test_user):
    with pytest.raises(TodoNotFound):
        service.get_todo(db, test_user.id, uuid.uuid4())


def test_update(db, test_user):
    todo = service.create_todo(db, test_user.id, TodoCreate(title="Old"))
    updated = service.update_todo(db, test_user.id, todo.id, TodoUpdate(title="New"))
    assert updated.title == "New"


def test_update_missing_raises(db, test_user):
    with pytest.raises(TodoNotFound):
        service.update_todo(db, test_user.id, uuid.uuid4(), TodoUpdate(title="Nope"))


def test_delete(db, test_user):
    todo = service.create_todo(db, test_user.id, TodoCreate(title="Temporary"))
    service.delete_todo(db, test_user.id, todo.id)

    with pytest.raises(TodoNotFound):
        service.get_todo(db, test_user.id, todo.id)


def test_list_filtered(db, test_user):
    service.create_todo(db, test_user.id, TodoCreate(title="A"))
    service.create_todo(db, test_user.id, TodoCreate(title="B", status="completed"))

    items, total = service.get_todos(db, test_user.id, status="completed")
    assert total == 1
    assert items[0].title == "B"


def test_list_paginated(db, test_user):
    for i in range(3):
        service.create_todo(db, test_user.id, TodoCreate(title=f"T{i}"))

    items, total = service.get_todos(db, test_user.id, page=2, page_size=2)
    assert total == 3
    assert len(items) == 1
