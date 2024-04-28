# from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, todoservice
from database.models import Todo
from pydantic import BaseModel

# Создание роутера для API задач
todo_router = APIRouter(prefix="/todos", tags=["Управление задачами"])


# Создание и обновления такса
class TodoModel(BaseModel):
    title: str
    description: str
    due_date: str


# Отправка запроса на создание задачи
@todo_router.post("/todos/create_todo")
async def create_todo(todo_model: Todo):
    todo_info = dict(todo_model)



# Получение списка задач
@todo_router.get("/todos/get_all_todos")
async def get_all_todos():
    pass


# Получение конкретной задачи
@todo_router.get("/todos/get_exact_todo")
async def get_exact_todo():
    pass


# Обновление задачи
@todo_router.put("/todos/update_todo")
async def update_todo():
    pass


# Удаление задачи
@todo_router.delete("/todos/delete_todo")
async def delete_todo():
    pass
