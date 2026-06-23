from flask import Blueprint, request, jsonify, redirect, url_for
from flask_login import logout_user, login_required
from app.services.register_service import register_user
from app.decorators import perfil_required
from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db

user_api_bp = Blueprint('user_api', __name__)

@user_api_bp.route("/register", methods=['POST'])
@perfil_required(UserProfile.SCHOLARSHIP, UserProfile.COORDINATOR)
def register():
    
    #obtenção dos dados do requisição
    data = request.get_json(silent=True)
    print("\nDados: ",data,flush=True)
    if not data:
        return jsonify({"success": False, "message": "Requisão Inválida."}), 400
    
    #separação dos dados e limpando espaços em branco
    username = data.get("Nome","").strip()
    email = data.get("Email","").strip()
    cpf = data.get("CPF","").strip()
    rg = data.get("RG","").strip()
    profession = data.get("Profissao","").strip()
    marital = data.get("Estado Civil","").strip()
    nationality = data.get("Nacionalidade","").strip()
    code_institutional = data.get("RA","").strip()
    street = data.get("Logradouro","").strip()
    neighborhood = data.get("Bairro","").strip()
    postal_code = data.get("CEP","").strip()
    number = data.get("Numero","").strip()
    city = data.get("Cidade","").strip()
    state = data.get("Estado","").strip()
    country = data.get("Pais","").strip()
    complement = data.get("complemento","").strip()
    sector = data.get("setor","").strip()
    position = data.get("cargo","").strip()
    profile = data.get("tipoUsuario","").strip()
    status = data.get("status","").strip()
    entry_at = data.get("dataEntrada","").strip()
    departure_at = data.get("dataSaida","").strip()
    
    #validação primária (da requisição em si)
    if not username or not email or not cpf or not rg or not profession or not marital or not nationality or not code_institutional or not street or not neighborhood or not postal_code or not number or not city or not state or not country or not complement or not sector or not position or not profile or not status or not entry_at:
        return jsonify({"success": False, "message": "Todos os campos obrigatórios devem ser preenchidos."}), 400
    
    #lógica da resolução de registro na camada de serviço
    result, status_code = register_user(username, email, cpf, rg, profession, marital, nationality, code_institutional, street, neighborhood, postal_code, number, city, state, country, complement, sector, position, profile, status, entry_at, departure_at)
    
    #retorno da resposta para o frontend
    return jsonify(result), status_code