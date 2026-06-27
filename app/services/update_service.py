from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db
from flask_login import current_user
from app.utils import parse_from_date

def update_user_from_user(data):
    
    # validar nome
    if not data.get(("Nome")or"").strip().replace(" ","").isalpha():
        return {"success": False, "message": "O nome de usuário deve conter apenas letras."}, 400
    
    # validar email
    if not (data.get("Email")or"").email_validate():
        return {"success": False, "message": "Email inválido."}, 400
    
    # validar rg
    if not (data.get("RG")or"").rg_validate(rg):
        return {"success": False, "message": "RG inválido."}, 400
    
    # validar profissão
    if not (data.get("Profissao")or"").replace(" ","").isalpha() or len((data.get("Profissao")or"")) > 100:
        return {"success": False, "message": "A profissão deve conter apenas letras."}, 400
    
    #validar estado civil
    if not ((data.get("Estado_Civil")or"") in [UserMarital.SINGLE.name, UserMarital.MARRIED.name, UserMarital.DIVORCED.name, UserMarital.WIDOWED.name, UserMarital.STABLE_UNION.name]):
        return {"success": False, "message": "Estado civil inválido."}, 400
    
    #validar nacionalidade
    if not (data.get("Nacionalidade")or"").replace(" ","").isalpha() or len((data.get("Nacionalidade")or"")) > 50:
        return {"success": False, "message": "A nacionalidade deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar RA
    if not (data.get("Registro_Academico")or"").isdigit() or len((data.get("Registro_Academico")or"")) > 20:
        return {"success": False, "message": "O RA deve conter apenas números e ser menor que 20 caracteres."}, 400
    
    #validar rua
    if not street.replace(" ","").isalpha() or len(street) > 150:
        return {"success": False, "message": "A rua deve conter apenas letras e ser menor que 150 caracteres."}, 400
    
    #validar bairro
    if not neighborhood.replace(" ","").isalpha() or len(neighborhood) > 100:
        return {"success": False, "message": "O bairro deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar cep
    if not postal_code.isdigit() or len(postal_code) != 8:
        return {"success": False, "message": "O CEP deve conter apenas números e ser composto por 8 caracteres."}, 400
    
    #validar número
    if not number.isdigit() or len(number) > 20:
        return {"success": False, "message": "O número deve conter apenas números e ser menor que 20 caracteres."}, 400
    
    #validar cidade
    if not city.replace(" ","").isalpha() or len(city) > 100:
        return {"success": False, "message": "A cidade deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar estado
    if not state.replace(" ","").isalpha() or len(state) > 100:
        return {"success": False, "message": "O estado deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar país
    if not country.replace(" ","").isalpha() or len(country) > 50:
        return {"success": False, "message": "O país deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar complemento
    # mudar a lógica para permitir que a data de sáida seja none
    if complement and (not complement.replace(" ","").isalnum() or len(complement) > 100):
        return {"success": False, "message": "O complemento deve conter apenas letras e números e ser menor que 100 caracteres."}, 400
    
    #validar setor
    if not sector in [UserSector.MARKETING.name, UserSector.RH.name, UserSector.CONTENT.name, UserSector.INSTRUCTORS.name]:
        return {"success": False, "message": "Setor inválido."}, 400
    
    #vaidar posição
    if not position in [UserPosition.STUDANT_COORDINATOR.name, UserPosition.REPRESENTATIVE.name, UserPosition.VOLUNTEER.name]:
        return {"success": False, "message": "Posição inválida."}, 400
    
    #validar tipo de usuário
    if not (profile in [UserProfile.COORDINATOR.name, UserProfile.SCHOLARSHIP.name, UserProfile.VOLUNTEER.name]):
        return {"success": False, "message": "Tipo de usuário inválido."}, 400
    
    #validar status
    if not status in [UserStatus.ACTIVE.name, UserStatus.INACTIVE.name, UserStatus.DELETED.name]:
        return {"success": False, "message": "Status inválido."}, 400
    
    old_user = current_user
    
    try:
        old_user.name = (data.get('Nome')or"").strip()
    
        db.session.commit()
        return {"success": True, "message": "Usuário Registrado com Sucesso."}, 201
    except:
        db.session.rollback()
        return {"success": False, "message": "Erro ao registrar usuário."}, 500
''