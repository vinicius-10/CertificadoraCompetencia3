"""API endpoints for user authentication and password recovery."""

import traceback

from flask import Blueprint, jsonify, redirect, request, url_for
from flask_login import login_required, logout_user

from app.services import authenticate_user, recovery_password_send, recovery_password_register

auth_api_bp = Blueprint('auth_api', __name__)


@auth_api_bp.route("/login", methods=['POST'])
def login():
    """
    Authenticate a user using credentials provided in a JSON request.

    The request body must contain the ``usuario`` and ``senha`` fields. An
    optional ``next_url`` field may be provided to define the destination
    after successful authentication.

    Returns:
        tuple: A JSON response and an HTTP status code indicating whether the
            request was valid and authentication succeeded.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Requisição inválida."}), 400
    
    username = data.get("usuario", "").strip()
    password = data.get("senha", "").strip()
    next_page = data.get("next_url", "")

    if not username or not password:
        return jsonify({"success": False, "message": "Usuário e senha são obrigatórios."}), 400
    
    result, status_code = authenticate_user(username, password, next_page)
    
    return jsonify(result), status_code


@auth_api_bp.route('/logout')
@login_required
def logout():
    """
    End the authenticated user's session.

    Returns:
        Response: A redirect response to the application's home page.
    """
    logout_user()
    return redirect(url_for("main.home"))


@auth_api_bp.route('/recovery', methods=['POST'])
def recovery():
    """
    Process a password recovery request.

    The request body must contain an ``email`` field. Valid requests are
    delegated to the authentication service, which generates and sends the
    password recovery email when the account exists.

    Returns:
        tuple: A JSON response and an HTTP status code indicating the result
            of the password recovery request.

    Notes:
        Unexpected exceptions are logged and returned as a generic server
        error to avoid exposing internal implementation details.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "message": "Requisição inválida."}), 400
        
        email = data.get('email', "").strip()
        if not email:
            return jsonify({"success": False, "message": "Email é obrigatório."}), 400
        
        result, status_code = recovery_password_send(email=email)
        
        return jsonify(result), status_code
    except Exception:
        traceback.print_exc()
        return jsonify({"success": False, "message": "Não foi possível conectar ao servidor. Tente novamente."}), 500


@auth_api_bp.route("recovery_password",  methods=['POST'])
def recovery_password():
    """
    Redefine a senha do usuário a partir de um token de recuperação.

    A rota recebe uma requisição POST com JSON contendo os campos
    ``Nova_senha``, ``Confirmar_senha`` e ``token``. Primeiro valida se a
    requisição possui corpo JSON, se os campos de senha foram preenchidos e se
    existe um token válido na requisição. Depois repassa os dados para o
    serviço responsável por validar o token e registrar a nova senha.

    Returns:
        tuple: Resposta JSON e código HTTP informando se a redefinição foi
            aceita, recusada por dados inválidos ou falhou por erro interno.

    Notes:
        Quando o token não é enviado, a resposta também inclui uma URL de
        redirecionamento para a tela de recuperação de senha.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"success": False, "message": "Requisição inválida."}), 400
        
        password = (data.get('Nova_senha') or '').strip()
        password_check = (data.get('Confirmar_senha') or '').strip()
        token = (data.get('token') or '').strip()
        
        if not password or not password_check:
            return jsonify({"success": False, "message": "Preencha todos os campos."}), 400
        
        if not token:
            return jsonify({"success": False, "message": "Token inválido ou ausente. Solicite um novo link de recuperação de senha.", "redirect": f"{url_for('main.RecuperacaoSenha')}"}), 400
        
        result, status_code = recovery_password_register(password=password, password_check=password_check, token=token)
        
        return jsonify(result), status_code
    except Exception:
        traceback.print_exc()
        return jsonify({"success": False, "message": "Não foi possível conectar ao servidor. Tente novamente."}), 500
