from sqlalchemy.orm import Session
from .models import Todo
from datetime import datetime


# Функция для создания задачи
def create_todo_database(db: Session, title: str, description: str, due_date: str, user_id: int):
    due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
    new_todo = Todo(title=title,
                    description=description,
                    due_date=due_date_obj,
                    owner_id=user_id,
                    created_date=datetime.now())
    db.add(new_todo)
    db.commit()
    return new_todo.id


# Функция для получения списка задач пользователя
def get_all_todos_database(db: Session, user_id: int):
    return db.query(Todo).filter(owner_id=user_id).all()


# Функция для получения задачи по id
def get_exact_todo_database(db: Session, todo_id: int):
    return db.query(Todo).filter(id=todo_id).first()


# Функция для обновления задачи
def update_todo(db: Session, todo_id: int, title: str, description: str, due_date: str, is_complete: bool):
    todo = get_exact_todo_database(db, todo_id)
    if todo:
        todo.title = title
        todo.description = description
        todo.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        todo.is_complete = is_complete
        db.commit()
        return todo
    else:
        return "Задача не найдена"


# Функция для удаления задачи
def delete_todo(db: Session, todo_id: int):
    todo = get_exact_todo_database(db, todo_id)
    if todo:
        db.delete(todo)
        db.commit()
        return "Удалена успешно"
    else:
        return "Задача не найдена"
