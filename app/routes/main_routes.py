
from app.utils import perfil_required
from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import db, User, Address, UserProfile, UserMarital, UserSector, UserPosition, UserStatus
from datetime import datetime, timezone
from sqlalchemy import func, select


main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def home():
    project_start_year = 2023
    years = datetime.now(timezone.utc).year - project_start_year
    
    active_scholars = db.session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.profile == UserProfile.SCHOLARSHIP, User.status == UserStatus.ACTIVE)
    )
    
    active_volunteers = db.session.scalar(
        select(func.count())
        .select_from(User)
        .where(User.profile == UserProfile.VOLUNTEER, User.status == UserStatus.ACTIVE)
    ) + active_scholars
    

    return render_template(
        "landing_page.html",
        years=years,
        active_volunteers=active_volunteers,
        active_scholars=active_scholars,
    )

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
    user_id=current_user.id
    return render_template("paginaADM.html",user_id=user_id, UserProfile=UserProfile, UserPosition=UserPosition, UserSector=UserSector  )


@main_bp.route("/cadastro")
@perfil_required(UserProfile.SCHOLARSHIP, UserProfile.COORDINATOR)
def cadastro():
    
    current_profile_coedinator = (current_user.profile == UserProfile.COORDINATOR)

    return render_template("cadastro.html", UserMarital=UserMarital, UserProfile=UserProfile, UserSector=UserSector, UserPosition=UserPosition, current_profile_coedinator=current_profile_coedinator, UserStatus= UserStatus)



@main_bp.route("/editVolunteer")
@perfil_required(UserProfile.VOLUNTEER, UserProfile.SCHOLARSHIP)
def edit_volunteer():
    
    marital_options = {e.name: "" for e in UserMarital}
    
    
    user = User.query.filter(
        User.id == current_user.id,
        User.status != UserStatus.DELETED
    ).first()
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    return render_template("Atualizacao_info_Volun.html", user=user, address=address, UserMarital=UserMarital, marital_options=marital_options)


@main_bp.route("/editADM", methods=['GET'])
@perfil_required(UserProfile.COORDINATOR, UserProfile.SCHOLARSHIP)
def edit_adm():
    user_id = request.args.get('user_id', '').strip()
    
    
    
    
    user = User.query.filter(User.id == user_id, User.status != UserStatus.DELETED).first()
    if not user:
        flash("Usuário não encontrado.", "error")
        return redirect(url_for("main.login"))
    
    marital_options = {e.name: "" for e in UserMarital}
    position_option = {e.name: "" for e in UserPosition}
    profile_option = {e.name: "" for e in UserProfile}
    status_option = {e.name: "" for e in UserStatus}
    sector_option = {e.name: "" for e in UserSector}
    
    current_profile_coedinator = (current_user.profile == UserProfile.COORDINATOR)
    
    address = Address.query.filter_by(user_id=user.id).first()
    
    marital_options[user.marital.name] = "selected"
    position_option[user.position.name] = "selected"
    profile_option[user.profile.name] = "selected"
    status_option[user.status.name] = "selected"
    sector_option[user.sector.name] = "selected"
    
    entry_at = datetime.strftime(user.entry_at, "%Y-%m-%d")
    departure_at = datetime.strftime(user.departure_at, "%Y-%m-%d") if user.departure_at else ''
    self_update =  user.id == current_user.id 
    
    
    return render_template("Atualizacao_info_ADM.html", user=user, address=address, UserMarital=UserMarital, UserPosition=UserPosition, UserProfile=UserProfile, UserStatus=UserStatus, UserSector=UserSector, marital_options=marital_options, position_option=position_option, profile_option=profile_option, status_option=status_option, sector_option=sector_option, current_profile_coedinator=current_profile_coedinator,entry_at=entry_at,departure_at=departure_at, self_update=self_update)


@main_bp.route("/emailSent")
def email_sent():
    return render_template("recuperacao_email.html")
