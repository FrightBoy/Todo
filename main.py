from fastapi import FastAPI
from database import Base, engine
from fastapi.staticfiles import StaticFiles

# APIs import
from API.user_api.user_api import user_router
# from API.todo_api.todo_api import todo_router

# команда для создания всех таблиц в дб
Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/")
app.mount("/static", StaticFiles(directory="static"))

app.include_router(user_router)
# app.include_router(todo_router)
