# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:superman@127.0.0.1:3306/music"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100), unique=True)
    created_time = db.Column(db.DateTime)


def create_user():
    user = User(
        id=1,
        name="hc",
        pwd=generate_password_hash("123456")
    )
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_user()
