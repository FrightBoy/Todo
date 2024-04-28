from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, todoservice
from database.security import verify_token
from database.models import Todo

# Создание роутера для API задач
todo_router = APIRouter(prefix="/todos", tags=["Управление задачами"])


# Отправка запроса на создание задачи
@todo_router.post("/", response_model=Todo)
async def create_todo(token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = verify_token(token)
    if payload == "error":
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя не найден в токене")
    # Создание задачи
    return todoservice.create_todo(db, create_todo, user_id)


# Получение списка задач
@todo_router.get("/", response_model=list[Todo])
async def read_todos(token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = verify_token(token)
    if payload == "error":
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя не найден в токене")
    # Получение списка задач пользователя
    return todoservice.get_todos(db, user_id)


# Получение конкретной задачи
@todo_router.get("/{todo_id}", response_model=Todo)
async def read_todo(todo_id: int, token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = verify_token(token)
    if payload == "error":
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя не найден в токене")
    # Получение задачи
    todo = todoservice.get_todo(db, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    # Проверка прав доступа
    if todo.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    return todo


# Обновление задачи
@todo_router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: create_todo, token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = verify_token(token)
    if payload == "error":
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя не найден в токене")
    # Получение задачи для проверки прав доступа
    existing_todo = todoservice.get_todo(db, todo_id)
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    if existing_todo.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Нет прав доступа")
    # Обновление задачи
    updated_todo = todoservice.update_todo(db, todo_id, todo)
    return updated_todo


# Удаление задачи
@todo_router.delete("/{todo_id}")
async def delete_todo(todo_id: int, token: str, db: Session = Depends(get_db)):
    # Проверка токена
    payload = verify_token(token)
    if payload == "error":
        raise HTTPException(status_code=401, detail="Неверный токен")
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="ID пользователя не найден в токене")
    # Удаление задачи
    deleted_todo = todoservice.delete_todo(db, todo_id)
    if deleted_todo is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    # Проверяем, принадлежит ли задача пользователю
    if deleted_todo.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Нет прав доступа к этой задаче")
    return {"status": "success", "message": "Задача удалена"}
