from .models import Todo
from database import get_db
from datetime import datetime, timedelta


# create todo in database

def create_todo_database(title, description, due_date, is_complete=False):
    db = next(get_db())
    expiration_time = datetime.now() + timedelta(days=due_date)
    new_todo = Todo(title=title, description=description, is_complete=is_complete, due_date=expiration_time,
                    created_date=datetime.now())
    db.add(new_todo)
    db.commit()
    return new_todo.id


# get all todos from database
def get_all_todos_database(owner_id):
    db = next(get_db())
    all_todos = db.query(Todo).filter_by(owner_id=owner_id).all()
    return all_todos


# get one todo from database
def get_exact_todo_database(todo_id):
    db = next(get_db())
    exact_todo = db.query(Todo).filter_by(id=todo_id).first()
    return exact_todo


# delete todo from database
def delete_todo_database(todo_id):
    db = next(get_db())
    db.query(Todo).filter_by(id=todo_id).delete()
    db.commit()
    return "Todo deleted"
