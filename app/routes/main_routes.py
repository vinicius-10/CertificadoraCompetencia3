
from app.decorators import perfil_required
from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app.models import UserProfile, db, User, Address
from datetime import datetime, timedelta, timezone


main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    years = (datetime.now(timezone.utc) - timedelta(days=2023*365)).year
    return render_template("landing_page.html", years=years)

@main_bp.route("/ping")
def ping():
    return {"status": "ok", "message": "pong"}


@main_bp.route("/login")
def login():
    if current_user.is_authenticated:
        if current_user.profile == UserProfile.VOLUNTEER:
            return redirect(url_for("main.user_view"))
        elif current_user.profile in [UserProfile.COORDINATOR, UserProfile.SCHOLARSHIP]:
            return redirect(url_for("main.admin_view"))
        
        else:
            return redirect(url_for("api.auth_api.logout"))
        
    return render_template("login.html")

@main_bp.route("/RecuperacaoSenha")
def RecuperacaoSenha():
    return render_template("RecuperacaoSenha.html")

@main_bp.route("/RedefinirSenha")
def reset_password():
    return render_template("RedefinicaoSenha.html")

@main_bp.route("/userView")
@perfil_required(UserProfile.VOLUNTEER)
def user_view():
    address = Address.query.filter_by(user_id=current_user.id).first()
    return render_template("visualizacaoUsuario.html",user=current_user, address=address)


@main_bp.route("/adminView")
@perfil_required(UserProfile.SCHOLARSHIP, UserProfile.COORDINATOR)
def admin_view():
    return render_template("paginaADM.html")


@main_bp.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")



@main_bp.route("/editVolunteer")
@perfil_required(UserProfile.VOLUNTEER, UserProfile.SCHOLARSHIP)
def edit_volunteer():
    from app.models import UserMarital
    marital_options = {e.name: "" for e in UserMarital}
    
    
    user = User.query.filter_by(id=current_user.id).first()
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    return render_template("Atualizacao_info_Volun.html", user=user, address=address, UserMarital=UserMarital, marital_options=marital_options)


@main_bp.route("/editADM")
@perfil_required(UserProfile.COORDINATOR, UserProfile.SCHOLARSHIP)
def edit_adm():
    from app.models import UserMarital
    marital_options = {e.name: "" for e in UserMarital}
    
    
    user = User.query.filter_by(id=current_user.id).first()
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    return render_template("Atualizacao_info_ADM.html", user=user, address=address, UserMarital=UserMarital, marital_options=marital_options)


@main_bp.route("/emailSent")
def email_sent():
    return render_template("recuperacao_email.html")