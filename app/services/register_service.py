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
    if not username.replace(" ","").isalpha():
        return {"success": False, "message": "O nome de usuário deve conter apenas letras."}, 400
    
    # validar email
    if not User.validate_email(email):
        return {"success": False, "message": "Email inválido."}, 400
    
    # validar rg
    if not User.rg_validate(rg):
        return {"success": False, "message": "RG inválido."}, 400
    
    # validar profissão
    if not profession.replace(" ","").isalpha() and len(profession) > 100:
        return {"success": False, "message": "A profissão deve conter apenas letras."}, 400
    
    #validar estado civil
    if not marital in [UserProfile.SINGLE, UserProfile.MARRIED, UserProfile.DIVORCED, UserProfile.WIDOWED, UserProfile.STABLE_UNION]:
        return {"success": False, "message": "Estado civil inválido."}, 400
    
    #validar nacionalidade
    if not nationality.replace(" ","").isalpha() and len(nationality) > 50:
        return {"success": False, "message": "A nacionalidade deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar RA
    if not code_institutional.isdigit() and len(code_institutional) > 20:
        return {"success": False, "message": "O RA deve conter apenas números e ser menor que 20 caracteres."}, 400
    
    #validar rua
    if not street.replace(" ","").isalpha() and len(street) > 150:
        return {"success": False, "message": "A rua deve conter apenas letras e ser menor que 150 caracteres."}, 400
    
    #validar bairro
    if not neighborhood.replace(" ","").isalpha() and len(neighborhood) > 100:
        return {"success": False, "message": "O bairro deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar cep
    if not postal_code.isdigit() and len(postal_code) != 8:
        return {"success": False, "message": "O CEP deve conter apenas números e ser composto por 8 caracteres."}, 400
    
    #validar número
    if not number.isdigit() and len(number) > 20:
        return {"success": False, "message": "O número deve conter apenas números e ser menor que 20 caracteres."}, 400
    
    #validar cidade
    if not city.replace(" ","").isalpha() and len(city) > 100:
        return {"success": False, "message": "A cidade deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar estado
    if not state.replace(" ","").isalpha() and len(state) > 100:
        return {"success": False, "message": "O estado deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar país
    if not country.replace(" ","").isalpha() and len(country) > 50:
        return {"success": False, "message": "O país deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar complemento
    if not complement.replace(" ","").isalnum() and len(complement) > 100:
        return {"success": False, "message": "O complemento deve conter apenas letras e números e ser menor que 100 caracteres."}, 400
    
    #validar setor
    if not sector in [UserSector.MARKETING, UserSector.RH, UserSector.CONTENT, UserSector.INSTRUCTORS]:
        return {"success": False, "message": "Setor inválido."}, 400
    
    #vaidar posição
    if not position in [UserPosition.STUDANT_COORDINATOR, UserPosition.REPRESENTATIVE, UserPosition.VOLUNTEER]:
        return {"success": False, "message": "Posição inválida."}, 400
    
    #validar tipo de usuário
    if not profile in [UserProfile.COORDINATOR, UserProfile.SCHOLARSHIP, UserProfile.VOLUNTEER]:
        return {"success": False, "message": "Tipo de usuário inválido."}, 400
    
    #validar status
    if not status in [UserStatus.ACTIVE, UserStatus.INACTIVE, UserStatus.DELETED]:
        return {"success": False, "message": "Status inválido."}, 400
    
    #validar data de entrada
    
    