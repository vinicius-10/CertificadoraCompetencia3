"""Service functions for authentication and password recovery flows."""

from urllib.parse import urlsplit

from flask import current_app, url_for, render_template
from flask_login import login_user

from app.models import AccessLog, PasswordRecoveryToken, User, UserBlock, UserProfile, db, UserStatus
from app.services.email_service import send_email
import time

def authenticate_user(username, password, next_page) -> tuple:
    """
    Authenticates a user and determines the appropriate redirect destination.

    This function normalizes the CPF, validates the provided credentials,
    searches only active users, verifies whether the account is temporarily
    blocked, records each login attempt, and authenticates the user when the
    password is correct. When authentication succeeds, the function returns a
    safe next page or the default page associated with the user's profile.

    Args:
        username (str): CPF submitted as the login identifier.
        password (str): Password submitted for authentication.
        next_page (str): Optional page requested before authentication.

    Returns:
        tuple: A response dictionary and HTTP status code indicating whether
            authentication succeeded, failed, or was blocked.
    """
    MAX_LOGIN_ATTEMPTS = current_app.config['MAX_LOGIN_ATTEMPTS']
    MINUTES_BLOCKED = current_app.config['MINUTES_BLOCKED']

    username = ''.join(filter(str.isdigit, username))
    #validação de entrada
    bool_string = isinstance(username, str) and isinstance(password, str)
    bool_cpf_validate = User.validate_cpf(username)
    bool_password_length =  len(password) <= 250 and len(password) >= 6

    if((bool_string and bool_cpf_validate and bool_password_length)):
        #obetm dados do usuário com base no cpf (username) (o retorno padrão é uma lista de objetos, como quero só um, uso o first())
        user = User.query.filter(User.cpf == username, User.status == UserStatus.ACTIVE).first()
        
        if user:
            #Chama a lógica que verifica se o usuário está bloqueado
            minutes_block = UserBlock.get_block_by_user(user)
            if minutes_block:
                return {"success": False, "message": f"Usuário bloqueado. Tente novamente em {minutes_block} minutos."}, 403
            
            #Tenta autenticar
            authenticated = user.check_password(password)
            AccessLog.register_attempt(user=user, username_attempt=username, is_successful=authenticated)
            
            if authenticated:
                login_user(user)
                
                #Define paagina para redirecionamento seguro
                if next_page and urlsplit(next_page).netloc == '' and not next_page.startswith('//'):
                    page = next_page
                else:
                    if user.profile == UserProfile.VOLUNTEER:
                        page = "/userView"
                    else:
                        page = "/adminView"
                    
                return {"success": True, "redirect": page}, 200
            
            else:
                #Trata erro de senha e possível bloqueio
                attempts = AccessLog.count_access_attempts(user=user)
                if attempts >= MAX_LOGIN_ATTEMPTS:
                    UserBlock.block_user(user=user)
                    return {"success": False, "message": f"Usuário bloqueado devido a múltiplas tentativas. Tente novamente em {MINUTES_BLOCKED} minutos."}, 403
        else:
            # Registro de tentativa para usuário inexistente
            AccessLog.register_attempt(username_attempt=username, is_successful=False)

    return {"success": False, "message": "Usuário ou senha incorretos."}, 401


def recovery_password_send(email) -> tuple:
    """
    Handles the password recovery request for a registered user.

    This function validates the provided email address, searches for an
    associated user account, creates a password recovery token when the user
    exists, and sends a password reset link by email. To avoid disclosing
    whether an email address is registered, the function returns the same
    generic success response when the email is valid but no user is found.

    Args:
        email (str): Email address submitted for password recovery.

    Returns:
        tuple: A response dictionary and HTTP status code indicating whether
            the recovery request was processed successfully.
    """
    valited_email = User.email_validate(email)
    if not valited_email:
        return {"success": False, "message": "Informe um email valido"}, 401
    
    user = User.query.filter(User.email == valited_email, User.status != UserStatus.DELETED).first()
    
    if user:
        password_recovery = PasswordRecoveryToken(
            user=user
        )
        db.session.add(password_recovery)
        db.session.commit()
        
        token = password_recovery.token
        expires_at = password_recovery.expires_at

        subject = "Recuperação de Senha - Meninas Hub"
        link = url_for('main.reset_password', token=token, _external=True)
        time_expiration = current_app.config['TOKEN_EXPIRATION_TIME']
        
        body = render_template("recuperacao_email.html", nome_usuario=user.name, link_redefinicao=link, tempo_expiracao=time_expiration, hora_limite=expires_at)
        
        code = send_email(to=user.email, subject=subject, body_html=body)
        
        if code == 0:
            return {"success": False, "message": "Não foi possível enviar o e-mail. Tente novamente mais tarde."}, 401
        else:
            return {"success": True, "message": "Caso o e-mail esteja cadastrado, um link de redefinição foi enviado. Lembre-se de verificar a pasta de spam."}, 200
    else:
        time.sleep(2)
        return {"success": True, "message": "Caso o e-mail esteja cadastrado, um link de redefinição foi enviado. Lembre-se de verificar a pasta de spam."}, 200


def recovery_password_register(password, password_check, token):
    """
    Register a new password using a valid password recovery token.

    This function looks up the recovery token, checks whether it exists and is
    still valid, validates the password confirmation and accepted password
    length, updates the associated user's password, and marks the token as
    used so it cannot be reused.

    Args:
        password (str): New password submitted by the user.
        password_check (str): Confirmation of the new password.
        token (str): Password recovery token sent by email.

    Returns:
        tuple: A response dictionary and HTTP status code indicating whether
            the password reset succeeded or why it was rejected.
    """
    token_object = PasswordRecoveryToken.query.filter(PasswordRecoveryToken.token == token).first()

    if not token_object or not token_object.is_valid():
        return {"success": False, "message": "Token inválido. Solicite um novo link de recuperação de senha.", "redirect": f"{url_for('main.RecuperacaoSenha')}"}, 400

    if password != password_check:
        return {"success": False, "message": "As senhas devem ser iguais."}, 400
    
    if  len(password) < 6:
        return {"success": False, "message": "A senha devem ter 6 ou mais caracteres."}, 400
    
    if len(password) >= 250 :
        return {"success": False, "message": "A senha devem ter menos de 250 caracteres."}, 400
    
    
    user = User.query.filter(User.id == token_object.user_id, User.status != UserStatus.DELETED).first()
    if not user:
        return  {"success": False, "message": "Usuario não encontrado."}, 400
    
    user.set_password(password)
    token_object.is_used = True
    
    db.session.commit()

    return {"success": True, "message": "Senha atualizada com sucesso.", "redirect": f"{url_for('main.login')}"}, 200
