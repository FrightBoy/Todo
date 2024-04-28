from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, todoservice
from database.models import Todo
from pydantic import BaseModel

todo_router = APIRouter(prefix="/todos", tags=["Управление задачами"])


class TodoModel(BaseModel):
    title: str
    description: str
    due_date: datetime


@todo_router.post("/create_todo")
async def create_todo(todo_model: TodoModel, db: Session = Depends(get_db)):
    todo_info = dict(todo_model)
    todo = Todo(**todo_info)
    db.add(todo)
    db.commit()
    return {"message": "Задача создана успешно"}


# получение всех задач
@todo_router.get("/get_all_todos")
async def get_all_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return [{"id": todo.id, "title": todo.title, "description": todo.description, "due_date": todo.due_date} for todo in
            todos]


# получение конкретной задачи
@todo_router.get("/get_exact_todo/{todo_id}")
async def get_exact_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return {"id": todo.id, "title": todo.title, "description": todo.description, "due_date": todo.due_date}


# обновление задачи
@todo_router.put("/update_todo/{todo_id}")
async def update_todo(todo_id: int, todo_model: TodoModel, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = todo_model.title
    todo.description = todo_model.description
    todo.due_date = todo_model.due_date
    db.commit()
    return {"message": "Задача обновлена успешно"}


# удаление задачи
@todo_router.delete("/delete_todo/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db.delete(todo)
    db.commit()
    return {"message": "Задача удалена успешно"}
