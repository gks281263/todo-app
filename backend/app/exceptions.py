from fastapi import Request
from fastapi.responses import JSONResponse


class TodoNotFound(Exception):
    def __init__(self, todo_id):
        self.todo_id = todo_id
        super().__init__(f"todo {todo_id} not found")


async def not_found_handler(request: Request, exc: TodoNotFound):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
