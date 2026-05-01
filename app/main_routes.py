
from flask import render_template, Blueprint, jsonify
from models import db, User, Address

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    return render_template("landing_page.html")

@main_bp.route("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@main_bp.route("/login")
def login():
    return render_template("login.html")