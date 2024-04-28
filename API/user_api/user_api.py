from fastapi import Request, APIRouter
from pydantic import BaseModel
from typing import List, Dict
from database.userservice import (register_user_database, check_user_database, check_user_password_database,
                                  change_user_info_database, profile_info_database, login_user_db)

import re
user_router = APIRouter(prefix='/users', tags=['Управление пользователями'])

regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def mail_checker(email):
    if re.fullmatch(regex, email):
        return True
    else:
        return False


class User(BaseModel):
    name: str
    email: str
    password: str


@user_router.post("/api/registration")
async def register_user(user_model: User):
    user_data = dict(user_model)
    mail_validation = mail_checker(user_model.email)
    check = check_user_database(email=user_model.email)
    if mail_validation:
        if check:
            try:
                reg_user = register_user_database(**user_data)
                return {"status": 1, "user_id": reg_user}
            except Exception as e:
                return {"status": 0, "message":  e}
    else:
        return {"status": 0, "message": "Invalid email or phone number"}


# получение данных о пользователе
@user_router.get("/api/user")
async def get_user(user_id: int):
    exact_user = profile_info_database(user_id=user_id)
    return {"status": 1, "message": exact_user}


# вход в аккаунт
@user_router.post("/api/user")
async def login_user(email: str, password: str):
    mail_validator = mail_checker(email)
    login = login_user_db(email=email, password=password)
    if mail_validator:
        login_checker = check_user_password_database(email=email, password=password)
        if login_checker.isdigit():
            return {"status": 1, "message": login_checker}
        return {"status": 0, "message": login_checker}
    return {"status": 0, "message": "Invalid email"}


# запрос на изменение информации о юзере
@user_router.put("/api/change_profile")
async def change_user_profile(user_id: int, change_info: str, new_data: str):
    data = change_user_info_database(user_id=user_id, change_info=change_info, new_data=new_data)
    return {"status": 1, "message": data}
