from fastapi import APIRouter
from pydantic import BaseModel
from database.userservice import (register_user_database, check_user_database, check_user_password_database,
                                  change_user_info_database, profile_info_database, login_user_database)

import re
user_router = APIRouter(prefix='/users', tags=['Управление пользователями'])

regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


# проверка валидности email
def mail_checker(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


#
class User(BaseModel):
    name: str
    email: str
    password: str


# запрос на регистрацию нового пользователя
@user_router.post("/api/registration")
async def register_user(user_model: User):
    user_data = dict(user_model)
    mail_validation = mail_checker(user_model.email)
    check = check_user_database(email=user_model.email)
    if mail_validation:
        if check:
            try:
                registration = register_user_database(**user_data)
                return {"status": 1, "user_id": registration}
            except Exception as e:
                return {"status": 0, "message":  e}
    else:
        return {"status": 0, "message": "Invalid email or phone number"}


# получение данных о пользователе
@user_router.get("/api/user")
async def get_user(user_id: int):
    get_him = profile_info_database(user_id=user_id)
    return {"status": 1, "message": get_him}


# вход в аккаунт
@user_router.post("/api/user")
async def login_user(email: str, password: str):
    mail_validator = mail_checker(email)
    if mail_validator:
        login_checker = check_user_password_database(email=email, password=password)
        if login_checker:
            login = login_user_database(email=email)
            return {"status": 1, "message": login}
        return {"status": 0, "message": login_checker}
    return {"status": 0, "message": "Invalid email"}


# запрос на изменение информации о юзере
@user_router.put("/api/change_profile")
async def change_user_profile(user_id: int, change_info: str, new_data: str):
    change = change_user_info_database(user_id=user_id, change_info=change_info, new_data=new_data)
    return {"status": 1, "message": change}
