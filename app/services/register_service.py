from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db
from flask_login import current_user


def register_user(username, email, cpf, rg, profession, marital, nationality, code_institutional, street, neighborhood, postal_code, number, city, state, country, complement, sector, position, profile, status, entry_at, departure_at):
    #verificar se o cpf é válido
    bool_cpf_validate = User.validate_cpf(cpf)
    if not bool_cpf_validate:
        return {"success": False, "message": "CPF inválido."}, 400
    
    
    # verifique se o usuário já existe com base no CPF
    existing_user = User.query.filter_by(cpf=cpf).first()
    if existing_user:
        return {"success": False, "message": "Usuário já registrado."}, 400
    
    # validar nome
    bool_name = username
    if not name.isalpha():
        return {"success": False, "message": "O nome de usuário deve conter apenas letras."}, 400
    
    # validar email
    bool_email = User.validate_email(email)