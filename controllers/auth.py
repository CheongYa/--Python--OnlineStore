from bson import ObjectId
from flask import request, render_template, flash, redirect, url_for, session
from .blueprint import user
from .blueprint import product
from models.user import User


def check_login():
    if not session.get('user_id'):
        return False

    user = User.find_one(session['user_id'])

    return user

def redirect_to_signin_form():
    flash('로그인이 필요합니다.')
    return redirect(url_for('user.signin_form'))

def is_admin():
    user = check_login() # 로그인 판단
    if not user:
        return False

    return user.get('is_admin', False) # get은 is_admin이 없다면 None을 리턴해줌, 지정했기에 False를 리턴