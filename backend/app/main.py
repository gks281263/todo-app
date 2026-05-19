import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.exceptions import TodoNotFound, not_found_handler
from app.routes import router

logging.basicConfig(level=settings.log_level, format="%(levelname)s %(name)s: %(message)s")

app = FastAPI(title="Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(TodoNotFound, not_found_handler)
app.include_router(router)
