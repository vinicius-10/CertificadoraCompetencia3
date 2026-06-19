
from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import logout_user, login_required
from app.services.auth_service import authenticate_user

auth_api_bp = Blueprint('auth_api', __name__)

@auth_api_bp.route("/login", methods=['POST'])
def login():
    #obtenção dos dados da requisição
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Requisição inválida."}), 400
    
    #separação dos dados e lipando espaços em branco
    username = data.get("usuario", "").strip()
    password = data.get("senha", "").strip()
    next_page = data.get("next_url", "")

    # Validação primária (da requisição em si)
    if not username or not password:
        return jsonify({"success": False, "message": "Usuário e senha são obrigatórios."}), 400
    
    #lógica da resolução de autenticação na camada de serviço
    result, status_code = authenticate_user(username, password, next_page)
    
    #retorno da resposta para o frontend
    return jsonify(result), status_code


@auth_api_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))