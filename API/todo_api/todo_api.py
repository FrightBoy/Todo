from fastapi import APIRouter
from pydantic import BaseModel
from database.todoservice import (create_todo_database,
                                  get_all_todos_database, get_exact_todo_database, delete_todo_database)

todo_router = APIRouter(prefix='/todos', tags=['Управление задачами'])


class Todo(BaseModel):
    title: str
    description: str
    due_date: int
    is_complete: bool = False


# запрос на создание новой задачи
@todo_router.post("/api/create-todo")
async def create_todo(todo_model: Todo):
    todo_data = dict(todo_model)
    try:
        new_todo = create_todo_database(**todo_data)
        return {"status": 1, "message": new_todo}
    except Exception as e:
        return {"status": 0, "message": e}


# запрос на получение всех задач
@todo_router.get("/api/todos")
async def get_all_todos():
    all_todos = get_all_todos_database(owner_id=1)
    return {"status": 1, "message": all_todos}


# запрос на получение конкретной задачи
@todo_router.get("/api/todo{todo_id}")
async def get_exact_todo(todo_id: int):
    exact_todo = get_exact_todo_database(todo_id=todo_id)
    return {"status": 1, "message": exact_todo}


# запрос на удаление задачи
@todo_router.delete("/api/todo-removing")
async def delete_todo(todo_id: int):
    delete_todo_database(todo_id=todo_id)
    return {"status": 1, "message": "Todo deleted"}
