from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import Base, engine
from API.user_api.user_api import user_router
from API.todo_api.todo_api import todo_router

# Создаем экземпляр приложения FastAPI
app = FastAPI()

# Подключаем статические файлы из папки "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключаем папку с шаблонами Jinja2
templates = Jinja2Templates(directory="templates")

# API роутеры
app.include_router(user_router)
app.include_router(todo_router)

# Команда для создания всех таблиц в базе данных
Base.metadata.create_all(bind=engine)


# Роут для отображения домашней страницы
@app.get("/", response_class=HTMLResponse)
async def get_home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Роут для отображения todo страницы
@app.get("/todo", response_class=HTMLResponse)
async def get_todo_list(request: Request):
    return templates.TemplateResponse("todo-list.html", {"request": request})

# Роут для отображения 404 страницы
@app.get("/404", response_class=HTMLResponse)
async def get_404_page(request: Request):
    return templates.TemplateResponse("404.html", {"request": request})

# Роут для отображения контактной страницы
@app.get("/contact", response_class=HTMLResponse)
async def get_contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

# Роут для отображения регистрации
@app.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

# Роут для отображения парольного сброса
@app.get("/password-reset", response_class=HTMLResponse)
async def get_password_reset_page(request: Request):
    return templates.TemplateResponse("password-reset.html", {"request": request})

# Роут для отображения 404 страницы
@app.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})




