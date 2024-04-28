from fastapi import FastAPI
from database import Base, engine
from API.user_api.user_api import user_router
from fastapi.staticfiles import StaticFiles

# команда для создания всех таблиц в дб
Base.metadata.create_all(bind=engine)
app = FastAPI(docs_url="/")
app.mount("/static", StaticFiles(directory="static"))

app.include_router(user_router)
