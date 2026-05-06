
from flask import Blueprint, request, jsonify
from flask_login import login_user
from models import UserProfile, db, User, AccessLog, UserBlock

api_bp = Blueprint('api', __name__)

@api_bp.route("/login", methods=['POST'])
def login():
    MAX_LOGIN_ATTEMPTS = 5
    WITHIN_MINUTES = 10
    MINUTES_BLOCKED = 15
    
    
    data = request.get_json(silent=True)
 
    if not data:
        return jsonify({"success": False, "message": "Requisição inválida."}), 400
    
    username = data.get("usuario", "").strip()
    password = data.get("senha", "").strip()
 
    if not username or not password:
        return jsonify({"success": False, "message": "Usuário e senha são obrigatórios."}), 400
    
    
    user = User.query.filter(
        (User.cpf == username) 
    ).first()
    
    if user:
        
        minutes_block = UserBlock.get_block_by_user(user)
        
        if minutes_block:
            return jsonify({"success": False, "message": f"Usuário bloqueado. Tente novamente em {minutes_block} minutos."}), 403
        
        authenticated = user.check_password(password)
        
        AccessLog.register_attempt(user=user,username_attempt=username, is_successful=authenticated)
        
        if authenticated:
            login_user(user)
           
            page = "/RecuperacaoSenha" if user.profile == UserProfile.ADMIN else "/RedefinirSenha"
            print(f"\n\n Login bem-sucedido para {user.profile}, mandando para {page}\n\n",flush=True)
            return jsonify({
                "success": True,
                "redirect": page,
            }), 200
            
        else:
            attempts = AccessLog.count_access_attempts(username=username, within_minutes=WITHIN_MINUTES)
            print(f"\n\n Tentativas de login para {username} nos últimos {WITHIN_MINUTES} minutos: {attempts}\n\n",flush=True)
            if(attempts >= MAX_LOGIN_ATTEMPTS):
                UserBlock.block_user(user=user, block_duration_minutes=MINUTES_BLOCKED)
                return jsonify({"success": False, "message": f"Usuário bloqueado devido a múltiplas tentativas de login. Tente novamente em {MINUTES_BLOCKED} minutos."}), 403
    
    if not user :               
        AccessLog.register_attempt(username_attempt=username, is_successful=False)
    return jsonify({"success": False, "message": "Usuário ou senha incorretos."}), 401 