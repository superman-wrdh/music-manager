# -*- coding:utf-8 -*-
from . import admin
from flask import render_template, url_for, redirect, g, request, abort,session
from flask_login import current_user, login_user, logout_user
from functools import wraps
from app.models import User


def admin_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token_header = request.headers.get('authorization')
        token = token_header[6:]  # 去掉格式中的Basic
        if token:
            g.current_user = User.verify_auth_token(token)
            if g.current_user.is_adminstractor():
                return f(*args, **kwargs)
            else:
                abort(403)
    return decorator


@admin.route("/")
def index():
    return redirect("/admin/login")


@admin.route("/login")
def login():
    return render_template("/admin/login.html")


@admin.route("/main")
def main():
    return render_template("/admin/main.html")


@admin.route("/add_session/<string:name>", methods=["POST", "GET"])
def add_session(name):
    print("name:", name)
    session["username"] = name
    return "<a href='#'>你好:"+name+"</a>"


@admin.route("/get_session", methods=["POST", "GET"])
def print_all_session():
    print("- get session -")
    content = []
    for i in session:
        print(session[i])
        content.append(i)
    return "----"

