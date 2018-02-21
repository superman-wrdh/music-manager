# -*- coding:utf-8 -*-
from flask import Flask,render_template
import pymysql
from flask_cors import *
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.debug = False
app.config['SECRET_KEY'] = "hcissuperman666"
app.config["upload_dir"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:superman@127.0.0.1:3306/music"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["url_prefix"] = "http://127.0.0.1:5000"
app.config["resource_api"] = "http://127.0.0.1:5000/resource/"

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint


@app.errorhandler(404)
def page_not_found(error):
    """
    404
    """
    return render_template("404.html"), 404


app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")
