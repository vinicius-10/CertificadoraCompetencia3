from app.models import User, UserBlock, AccessLog, UserProfile
from flask_login import login_user
from urllib.parse import urlsplit
from flask import current_app


def authenticate_user(username, password, next_page):
    MAX_LOGIN_ATTEMPTS = current_app.config['MAX_LOGIN_ATTEMPTS']
    MINUTES_BLOCKED = current_app.config['MINUTES_BLOCKED']

    username = ''.join(filter(str.isdigit, username))
    #validação de entrada
    bool_string = isinstance(username, str) and isinstance(password, str)
    bool_cpf_validate = User.validate_cpf(username)
    bool_password_length =  len(password) <= 250 and len(password) >= 6

    if((bool_string and bool_cpf_validate and bool_password_length)):
        #obetm dados do usuário com base no cpf (username) (o retorno padrão é uma lista de objetos, como quero só um, uso o first())
        user = User.query.filter(User.cpf == username).first()
        
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
                    
                print(f"\nRota: {page}, user {user.profile}\n", flush=True)
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