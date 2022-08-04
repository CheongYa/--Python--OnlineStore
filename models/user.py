from operator import truediv
from .mongodb import conn_mongodb
from datetime import datetime
from bson import ObjectId
from flask_bcrypt import generate_password_hash, check_password_hash # 비밀번호 암호화 용도

class User():
    @staticmethod
    def insert_one(form_data):
        db = conn_mongodb()
        password_hash = generate_password_hash(form_data['password'])
        db.users.insert_one({
            'email': form_data['email'],
            'password': password_hash,
            'created_at': int(datetime.now().timestamp()),
            'update_at': int(datetime.now().timestamp())
        })

    def check_email(email):
        db = conn_mongodb()
        user = db.users.find_one({'email': email})

        return False if user else True

    def sign_in(login_data):
        db = conn_mongodb()
        user = db.users.find_one({'email': login_data['email']})
        
        if not user:
            return False

        if not check_password_hash(user['password'], login_data['password']):
            return False

        return user