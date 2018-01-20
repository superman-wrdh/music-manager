# -*- coding:utf-8 -*-
from . import admin
from flask import render_template, url_for,redirect


@admin.route("/")
def index():
    return redirect("/admin/login")


@admin.route("/login")
def login():
    return render_template("/admin/login.html")


@admin.route("/main")
def main():
    return render_template("/admin/main.html")

