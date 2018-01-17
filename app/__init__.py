# -*- coding:utf-8 -*-
from flask import Flask
import os

app = Flask(__name__)
app.debug = False
app.config["upload_dir"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:superman@127.0.0.1:3306/music"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
