# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app

db = SQLAlchemy(app)


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100), unique=True)


class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    album = db.Column(db.String(100))
    cover = db.Column(db.String(100))
    mp3 = db.Column(db.String(100))
    ogg = db.Column(db.String(100))
    img = db.Column(db.String(100))
    create_time = db.Column(db.String(100))
    update_time = db.Column(db.String(100))


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    name = db.Column(db.String(255))
    original_file_name = db.Column(db.String(255))
    mime_type = db.Column(db.String(100))
    size = db.Column(db.String(100))
    description = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, default=datetime.now())


def create_user():
    user = User(
        id=2,
        name="hc2",
        pwd=generate_password_hash("123456")
    )
    db.session.add(user)
    db.session.commit()


def create_table():
    db.create_all()


if __name__ == '__main__':
    resource = Resource.query.filter_by(uuid="85952bb0-3379-4477-8256-a72d51092350").first()
    print(resource.uuid)
