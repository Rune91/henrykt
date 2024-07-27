from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from statapp.db.stat_db import myDB

BP = Blueprint(
    "index", __name__, static_folder="stat/static", template_folder="stat/templates"
)

@BP.route("/favicon.ico")
def favicon():
    return url_for("static", filename="imgs/icon/favicon.ico")

@BP.route("/")
def index():
    return redirect(url_for("feedback.options"))

