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
    if not (data.get("Logradouro")or"").replace(" ","").isalpha() or len((data.get("Logradouro")or"")) > 150:
        return {"success": False, "message": "A rua deve conter apenas letras e ser menor que 150 caracteres."}, 400
    
    #validar bairro
    if not (data.get("Bairro")or"").replace(" ","").isalpha() or len((data.get("Bairro")or"")) > 100:
        return {"success": False, "message": "O bairro deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar cep
    if not (data.get("CEP")or"").isdigit() or len((data.get("CEP")or"")) != 8:
        return {"success": False, "message": "O CEP deve conter apenas números e ser composto por 8 caracteres."}, 400
    
    #validar número
    if not (data.get("Numero")or"").isdigit() or len((data.get("Numero")or"")) > 20:
        return {"success": False, "message": "O número deve conter apenas números e ser menor que 20 caracteres."}, 400
    
    #validar cidade
    if not (data.get("Cidade")or"").replace(" ","").isalpha() or len((data.get("Cidade")or"")) > 100:
        return {"success": False, "message": "A cidade deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar estado
    if not (data.get("Estado")or"").replace(" ","").isalpha() or len((data.get("Estado")or"")) > 100:
        return {"success": False, "message": "O estado deve conter apenas letras e ser menor que 100 caracteres."}, 400
    
    #validar país
    if not (data.get("Pais")or"").replace(" ","").isalpha() or len((data.get("Pais")or"")) > 50:
        return {"success": False, "message": "O país deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar complemento
    if (data.get("Complemento")or"") and (not (data.get("Complemento")or"").replace(" ","").isalnum() or len((data.get("Complemento")or"")) > 100):
        return {"success": False, "message": "O complemento deve conter apenas letras e números e ser menor que 100 caracteres."}, 400
    
    old_user = current_user
    
    try:
        old_user.name = (data.get('Nome')or"").strip()
        old_user.email = (data.get("Email")or"").strip()
        old_user.profession = (data.get("Profissao")or"").strip()
        old_user.marital = (data.get("Estado_Civil")or"").strip()
        old_user.code_institutional = (data.get("Registro_Academico")or"").strip()
        old_user.nationality = (data.get("Nacionalidade")or"").strip()
        old_user.street = (data.get("Logradouro")or"").strip()
        old_user.neighborhood = (data.get("Bairro")or"").strip()
        old_user.postal_code = (data.get("CEP")or"").strip()
        old_user.number = (data.get("Numero")or"").strip()
        old_user.city = (data.get("Cidade")or"").strip()
        old_user.state = (data.get("Estado")or"").strip()
        old_user.country = (data.get("Pais")or"").strip()
        old_user.complement = (data.get("Complemento")or"").strip()
    
        db.session.commit()
        return {"success": True, "message": "Dados atualizados com Sucesso."}, 201
    except:
        db.session.rollback()
        return {"success": False, "message": "Erro ao atualizar dados."}, 500