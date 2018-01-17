# -*- coding:utf-8 -*-
from . import home
from app.models import Music , Resource
from flask import Flask, request, Response,jsonify
import os
from app import app
from pprint import pprint
from uuid import uuid4
from datetime import datetime
from app.models import db


@home.route("/")
def index():
    return "<h1 style='color:red'>this is home</h1>"


def get_file_type(filename):
    if filename.count(".") == 0:
        return ""
    return filename[filename.rindex("."):]


@home.route("/resource/<rid>")
def get_resource(rid):
    resource = Resource.query.filter_by(uuid=rid).first()
    basepath = app.config["upload_dir"]
    filepath = os.path.join(basepath, resource.name)
    local_resource = open(filepath, "rb")
    resp = Response(local_resource, mimetype=resource.mime_type)
    return resp


@home.route("/upload", methods=["POST"])
def upload():
    f = request.files['file']
    upload_path =app.config["upload_dir"]
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        os.chmod(upload_path, "rw")
    security_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f")+"-"+str(uuid4())+get_file_type(f.filename)
    f.save(os.path.join(upload_path, security_name))
    resource = Resource(
        uuid=str(uuid4()),
        name=security_name,
        original_file_name=f.filename,
        mime_type=f.mimetype,
        created_time=datetime.now()
    )
    db.session.add(resource)
    db.session.commit()
    return jsonify({"status": "success", "data": {"file": f.filename,
                    "mimetype": f.mimetype
                    }})
