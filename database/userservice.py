from .models import User
from database import get_db
from datetime import datetime
from database.security import create_access_token


# register user
def register_user_database(name, email, password):
    db = next(get_db())
    new_user = User(name=name, email=email, password=password, reg_date=datetime.now())
    db.add(new_user)
    db.commit()
    return new_user.id


# Checker for user in database
def check_user_database(email):
    db = next(get_db())
    checker = db.query(User).filter_by(email=email).first()
    if checker:
        return False
    return True


# check user password
def check_user_password_database(email, password):
    db = next(get_db())
    checker = db.query(User).filter_by(email=email).first()
    if checker:
        if checker.password == password:
            return checker.id
        else:
            return "Wrong password"
    else:
        return "Wrong email"


# get profile info
def profile_info_database(user_id):
    db = next(get_db())
    all_info = db.query(User).filter_by(id=user_id).first()
    if all_info:
        return all_info.email, all_info.name, all_info.reg_date
    return "User not found"


# Login for user
def change_user_info_database(user_id, change_info, new_data):
    db = next(get_db())
    all_info = db.query(User).filter_by(id=user_id).first()
    if all_info:
        if change_info == "name":
            all_info.name = new_data
        elif change_info == "email":
            all_info.email = new_data
        elif change_info == "password":
            all_info.password = new_data
        db.commit()
        return "Info updated"
    return "User not found"

# Logout for user
def login_user_db(email):
    db = next(get_db())
    login = db.query(User).filter_by(email=email).first()
    if login:
        token_data = {"user_id": login.id}
        access_token_data = create_access_token(token_data)
        return {"access_token": access_token_data, "token_type": "Bearer", "status": "Success"}
    else:
        return 'Wrong Login of Password'
