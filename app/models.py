# -*- coding:utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import app

db = SQLAlchemy(app)


def fill_url(uuid):
    return app.config["resource_api"] + uuid


# 用户
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    mail = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(100))
    #role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)


# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(64), unique=True)
#     permissions = db.Column(db.Integer)
#     default = db.Column(db.Boolean, default=False, index=True)
#     users = db.relationship('User', backref='role', lazy='dynamic')
#
#     def __repr__(self):
#         return '<Role %r>' % self.name
#
#     @staticmethod
#     def insert_role():
#         # 这里需要注意的是‘|’的用法，以及python对各种进制的处理
#         roles = {
#             'User': (Permission.FOLLOW |
#                      Permission.COMMENT |
#                      Permission.WRITE_ARTICLES, True),
#             'Moderate': (Permission.FOLLOW |
#                          Permission.COMMENT |
#                          Permission.WRITE_ARTICLES |
#                          Permission.MODERATE_COMMENTS, False),
#             'Administrator': (0xff, False)
#         }
#         for r in roles:
#             role = Role.query.filter_by(name=r).first()
#             if role is None:
#                 role = Role(name=r)
#             role.permissions = roles[r][0]
#             role.default = roles[r][1]
#             db.session.add(role)
#         db.session.commit()
#
#
# class Permission:
#     FOLLOW = 0x01
#     COMMENT = 0x02
#     WRITE_ARTICLES = 0x04
#     MODERATE_COMMENTS = 0x08
#     ADMINISTER = 0x80


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


def create_table():
    db.create_all()


def get():
    resource = Resource.query.filter_by(uuid="d28c4bc7-99a6-460e-8608-43b8899983e6").first()
    print(resource)


def get_music_list():
    music_list = [m.to_json() for m in Music.query.all()]
    print(music_list)


def create_user():
    user = User(
        name="hc",
        password="123456",
        mail="hc@163.com"
    )
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_table()
    #user = User.query.filter_by(id=1).first()
    #print(user.verify_password("123456"))

