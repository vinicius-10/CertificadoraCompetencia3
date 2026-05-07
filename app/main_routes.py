
from decorators import perfil_required
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from models import UserProfile, db, User, Address

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

@main_bp.route("/RecuperacaoSenha")
def RecuperacaoSenha():
    return render_template("RecuperacaoSenha.html")

@main_bp.route("/RedefinirSenha")
def reset_password():
    return render_template("RedefinicaoSenha.html")

@main_bp.route("/userView")
@perfil_required(UserProfile.VOLUNTEER, UserProfile.ADMIN, UserProfile.COORDINATOR)
def user_view():
    print(current_user.id,flush=True)
    
    user = User.query.filter_by(id=current_user.id).first()
    address = Address.query.filter_by(user_id=user.id).first()
    return render_template("visualizacaoUsuario.html",user=user, address=address)


@main_bp.route("/adminView")
@perfil_required(UserProfile.ADMIN, UserProfile.COORDINATOR)
def admin_view():
    return render_template("paginaADM.html")


@main_bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")
