# -*- coding:utf-8 -*-
from . import home
from app.models import Music, Resource
from flask import Flask, request, Response, jsonify, render_template,url_for
import os
from app import app
from pprint import pprint
from uuid import uuid4
from datetime import datetime
from app.models import db


@home.route("/")
def index():
    return render_template("/home/index.html")


def get_file_type(filename):
    if filename.count(".") == 0:
        return ""
    return filename[filename.rindex("."):]


@home.route("/resource/<rid>")
def get_resource(rid):
    print("in")
    resource = Resource.query.filter_by(uuid=rid).first()
    basepath = app.config["upload_dir"]
    filepath = os.path.join(basepath, resource.name)
    local_resource = open(filepath, "rb")
    resp = Response(local_resource, mimetype=resource.mime_type)
    return resp


@home.route("/upload", methods=["POST"])
def upload():
    f = request.files['file']
    file_info = save_file(f)

    return jsonify({"status": "success", "data": {"file": f.filename,
                                                  "mimetype": f.mimetype,
                                                  "uuid": file_info["uuid"]
                                                  }})


def save_file(file):
    upload_path = app.config["upload_dir"]
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
        os.chmod(upload_path, "rw")
    security_name = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f") + "-" + str(uuid4()) + get_file_type(
        file.filename)
    uuid = str(uuid4())
    resource = Resource(
        uuid=uuid,
        name=security_name,
        original_file_name=file.filename,
        mime_type=file.mimetype,
        created_time=datetime.now()
    )
    db.session.add(resource)
    db.session.commit()

    file.save(os.path.join(upload_path, security_name))
    return {"security_name": security_name, "mimetype": file.mimetype, "uuid": uuid}


@home.route("/upload/music", methods=["POST"])
def upload_music():
    music_file = request.files['mp3']
    img_file = request.files['img']
    cover_file = request.files['cover']

    music_file_info = save_file(music_file)
    img_file_info = save_file(img_file)
    cover_file_info = save_file(cover_file)

    title = request.form.get("title", music_file.filename)
    artist = request.form.get("artist", "")
    album = request.form.get("album", "")
    cover = cover_file_info["uuid"]
    mp3 = music_file_info["uuid"]
    img = img_file_info["uuid"]
    music = Music(
        title=title,
        artist=artist,
        album=album,
        cover=cover,
        mp3=mp3,
        img=img,
        create_time=datetime.now(),
        update_time=datetime.now()
    )
    db.session.add(music)
    db.session.commit()
    return jsonify({
        "status": "success",
        "data": {
            "title": title,
            "artist": artist,
            "album": album,
            "cover": cover,
            "mp3": mp3,
            "img": img,
        }
    })


@home.route("/music/list")
def music_list():
    music_list = [m.to_json() for m in Music.query.all()]
    return jsonify({"data": music_list})
