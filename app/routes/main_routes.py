
from app.utils import perfil_required
from flask import render_template, Blueprint, redirect, url_for
from flask_login import login_required, current_user
from app.models import UserProfile, db, User, Address, UserProfile, UserMarital, UserSector, UserPosition, UserStatus
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
@perfil_required(UserProfile.SCHOLARSHIP, UserProfile.COORDINATOR)
def cadastro():
    
    current_profile_coedinator = (current_user.profile == UserProfile.COORDINATOR)

    return render_template("cadastro.html", UserMarital=UserMarital, UserProfile=UserProfile, UserSector=UserSector, UserPosition=UserPosition, current_profile_coedinator=current_profile_coedinator, UserStatus= UserStatus)



@main_bp.route("/editVolunteer")
@perfil_required(UserProfile.VOLUNTEER, UserProfile.SCHOLARSHIP)
def edit_volunteer():
    
    marital_options = {e.name: "" for e in UserMarital}
    
    
    user = User.query.filter_by(id=current_user.id).first()
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    return render_template("Atualizacao_info_Volun.html", user=user, address=address, UserMarital=UserMarital, marital_options=marital_options)


@main_bp.route("/editADM")
@perfil_required(UserProfile.COORDINATOR, UserProfile.SCHOLARSHIP)
def edit_adm():
    marital_options = {e.name: "" for e in UserMarital}
    position_option = {e.name: "" for e in UserPosition}
    profile_option = {e.name: "" for e in UserProfile}
    status_option = {e.name: "" for e in UserStatus}
    sector_option = {e.name: "" for e in UserSector}
    
    current_profile_coedinator = (current_user.profile == UserProfile.COORDINATOR)
    user = current_user
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    position_option[user.position.name] = "selected"
    profile_option[user.profile.name] = "selected"
    status_option[user.status.name] = "selected"
    sector_option[user.sector.name] = "selected"
    
    entry_at = datetime.strftime(user.entry_at, "%Y-%m-%d")
    departure_at = datetime.strftime(user.departure_at, "%Y-%m-%d") if user.departure_at else ''
    
    return render_template("Atualizacao_info_ADM.html", user=user, address=address, UserMarital=UserMarital, UserPosition=UserPosition, UserProfile=UserProfile, UserStatus=UserStatus, UserSector=UserSector, marital_options=marital_options, position_option=position_option, profile_option=profile_option, status_option=status_option, sector_option=sector_option, current_profile_coedinator=current_profile_coedinator,entry_at=entry_at,departure_at=departure_at)


@main_bp.route("/emailSent")
def email_sent():
    return render_template("recuperacao_email.html")


    """
    
    <option value="{{UserMarital.SINGLE}}" {{marital_options[UserMarital.SINGLE.name]}}>{{UserMarital.SINGLE.value}}</option>
                                <option value="{{UserMarital.MARRIED}}" {{marital_options[UserMarital.MARRIED.name]}}>{{UserMarital.MARRIED.value}}</option>
                                <option value="{{UserMarital.DIVORCED}}" {{marital_options[UserMarital.DIVORCED.name]}}>{{UserMarital.DIVORCED.value}}</option>
                                <option value="{{UserMarital.WIDOWED}}" {{marital_options[UserMarital.WIDOWED.name]}}>{{UserMarital.WIDOWED.value}}</option>
                                <option value="{{UserMarital.STABLE_UNION}}"{{marital_options[UserMarital.STABLE_UNION.name]}}>{{UserMarital.STABLE_UNION.value}}</option>
    """