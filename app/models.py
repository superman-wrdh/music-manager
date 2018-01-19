# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app

db = SQLAlchemy(app)


def fill_url(uuid):
    return app.config["resource_api"]+uuid


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

    def to_json(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "cover": fill_url(self.cover),
            "mp3": fill_url(self.mp3),
            "img": fill_url(self.img)
        }


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    name = db.Column(db.String(255))
    original_file_name = db.Column(db.String(255))
    mime_type = db.Column(db.String(100))
    size = db.Column(db.String(100))
    description = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, default=datetime.now())

    def to_json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "original_file_name": self.original_file_name,
            "mime_type": self.mime_type,
            "description": self.description
        }


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


def get():
    resource = Resource.query.filter_by(uuid="d28c4bc7-99a6-460e-8608-43b8899983e6").first()
    print(resource)


def get_music_list():
    music_list = [m.to_json() for m in Music.query.all()]
    print(music_list)


if __name__ == '__main__':
    get_music_list()
