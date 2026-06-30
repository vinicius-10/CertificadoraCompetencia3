from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db
from flask_login import current_user
from flask import url_for
from app.utils import parse_from_date
import traceback

def update_user_from_user(data):
    
    # validar nome
    if not data.get(("Nome")or"").strip().replace(" ","").isalpha():
        return {"success": False, "message": "O nome de usuário deve conter apenas letras."}, 400
    
    # validar email
    if not User.email_validate((data.get("Email")or"")):
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
    
    #validar senha
    if  (data.get("Nova_senha")or"").strip():
        if (data.get("Nova_senha")or"").strip() != (data.get("Confirma_Senha")or"").strip():
            return {"success": False, "message": "As senhas devem ser iguais."}, 400

        if  len((data.get("Nova_senha")or"").strip()) < 6:
            return {"success": False, "message": "A senha devem ter 6 ou mais caracteres."}, 400

        if len((data.get("Nova_senha")or"").strip()) >= 250 :
            return {"success": False, "message": "A senha devem ter menos de 250 caracteres."}, 400
    
    old_user = current_user
    
    old_address = Address.query.filter_by(user_id=old_user.id).first()
    
    try:
        old_user.name = (data.get('Nome')or"").strip()
        old_user.email = (data.get("Email")or"").strip()
        old_user.profession = (data.get("Profissao")or"").strip()
        old_user.marital = UserMarital[(data.get("Estado_Civil")or"").strip()]
        old_user.code_institutional = (data.get("Registro_Academico")or"").strip()
        old_user.nationality = (data.get("Nacionalidade")or"").strip()
        old_address.street = (data.get("Logradouro")or"").strip()
        old_address.neighborhood = (data.get("Bairro")or"").strip()
        old_address.postal_code = (data.get("CEP")or"").strip()
        old_address.number = (data.get("Numero")or"").strip()
        old_address.city = (data.get("Cidade")or"").strip()
        old_address.state = (data.get("Estado")or"").strip()
        old_address.country = (data.get("Pais")or"").strip()
        old_address.complement = (data.get("Complemento")or"").strip()
        old_user.set_password((data.get("Nova_senha")or"").strip())
    
        db.session.commit()
        return {"success": True, "message": "Dados atualizados com Sucesso."}, 201
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return {"success": False, "message": "Erro ao atualizar dados."}, 500
    
def update_user_from_admin(data):
    
    #validação do usuário
    old_user = User.query.filter(User.id==((data.get("id")or"")).strip(), User.status != UserStatus.DELETED).first()
    if not old_user:
        return {"success": False, "message": "Usuário não encontrado."}, 404
    
    # validar nome
    if not data.get(("Nome")or"").strip().replace(" ","").isalpha():
        return {"success": False, "message": "O nome de usuário deve conter apenas letras."}, 400
    
    # validar email
    if not User.email_validate((data.get("Email")or"")):
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
    
    #validar setor
    if not (data.get("setor")or"") in [UserSector.MARKETING.name, UserSector.RH.name, UserSector.CONTENT.name, UserSector.INSTRUCTORS.name]:
        return {"success": False, "message": "Setor inválido."}, 400
    
    #vaidar posição
    if not (data.get("cargo")or"") in [UserPosition.STUDANT_COORDINATOR.name, UserPosition.REPRESENTATIVE.name, UserPosition.VOLUNTEER.name]:
        return {"success": False, "message": "Posição inválida."}, 400
    
    #validar tipo de usuário
    if not ((data.get("tipoUsuario")or"") in [UserProfile.COORDINATOR.name, UserProfile.SCHOLARSHIP.name, UserProfile.VOLUNTEER.name]):
        return {"success": False, "message": "Tipo de usuário inválido."}, 400
    
    #validar data de entrada
    data_entry = parse_from_date((data.get("dataEntrada")or"").strip())
    
    if not data_entry:
        return {"success": False, "message": "Data de entrada inválida."}, 400
    
    #validar data de saída
    data_departure = parse_from_date((data.get("dataSaida")or"").strip())
    if data_departure and data_departure < data_entry:
        return {"success": False, "message": "Data de saída inválida."}, 400
    
    #validar status
    if not (data.get("status")or"") in [UserStatus.ACTIVE.name, UserStatus.INACTIVE.name, UserStatus.DELETED.name]:
        return {"success": False, "message": "Status inválido."}, 400
    
    #se o status do coordenador atual for colocado em desligado mas ter somente ele de coordenador, não permitir a alteração
    if old_user.profile == UserProfile.COORDINATOR and (data.get("status")or"") == UserStatus.INACTIVE.name and (User.query.filter_by(profile=UserProfile.COORDINATOR, status=UserStatus.ACTIVE).count() == 1):
        return {"success": False, "message": "Não é possível inativar o único coordenador ativo."}, 400
    
    
    if (data.get("status")or"") == UserStatus.INACTIVE.name and not data_departure:
        return {"success": False, "message": "Data de saída é obrigatória para usuários inativos."}, 400
    
    #validar senha
    
    if (current_user.id == old_user.id):
        
        if (data.get("Nova_senha")or"").strip():
            if (data.get("Nova_senha")or"").strip() != (data.get("Confirma_Senha")or"").strip():
                return {"success": False, "message": "As senhas devem ser iguais."}, 400

            if  len((data.get("Nova_senha")or"").strip()) < 6:
                return {"success": False, "message": "A senha devem ter 6 ou mais caracteres."}, 400

            if len((data.get("Nova_senha")or"").strip()) >= 250 :
                return {"success": False, "message": "A senha devem ter menos de 250 caracteres."}, 400
    else:
        return {"success": False, "message": "Você não tem permissão para alterar a senha de outro usuário."}, 403
        
    old_address = Address.query.filter_by(user_id=old_user.id).first()
    
    try:
        old_user.name = (data.get('Nome')or"").strip()
        old_user.email = (data.get("Email")or"").strip()
        old_user.profession = (data.get("Profissao")or"").strip()
        old_user.marital = UserMarital[(data.get("Estado_Civil")or"").strip()]
        old_user.code_institutional = (data.get("Registro_Academico")or"").strip()
        old_user.nationality = (data.get("Nacionalidade")or"").strip()
        old_address.street = (data.get("Logradouro")or"").strip()
        old_address.neighborhood = (data.get("Bairro")or"").strip()
        old_address.postal_code = (data.get("CEP")or"").strip()
        old_address.number = (data.get("Numero")or"").strip()
        old_address.city = (data.get("Cidade")or"").strip()
        old_address.state = (data.get("Estado")or"").strip()
        old_address.country = (data.get("Pais")or"").strip()
        old_address.complement = (data.get("Complemento")or"").strip()
        old_user.sector = UserSector[(data.get("setor")or"").strip()]
        old_user.position = UserPosition[(data.get("cargo")or"").strip()]
        old_user.profile = UserProfile[(data.get("tipoUsuario")or"").strip()]
        old_user.status = UserStatus[(data.get("status")or"").strip()]
        old_user.entry_at = data_entry
        old_user.departure_at = data_departure
        old_user.set_password((data.get("Nova_senha")or"").strip())
    
        db.session.commit()
        return {"success": True, "message": "Dados atualizados com Sucesso."}, 201
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return {"success": False, "message": "Erro ao atualizar dados."}, 500
    
    
    
def delete_user_amd(data):
    user_id = (data.get("id") or "").strip()
    
    try:
        user = User.query.filter(User.id == user_id, User.status != UserStatus.DELETED).first()
        
        if not user:
            return {"success": False, "message": "Usuario não encontrado."}, 500
        
        if current_user.profile == UserProfile.SCHOLARSHIP and user.profile == UserProfile.COORDINATOR:
            return {"success": False, "message": "Somente um coordenador pode excluir outro coordenador."}, 500
            
        user.status = UserStatus.DELETED
        
        db.session.commit()
        
        return {"success": True, "message": "Usuario Excluido.", "redirect": url_for("main.admin_view")}, 200
    
    except Exception:
        traceback.print_exc()
        db.session.rollback()
        return {"success": False, "message": "Erro ao atualizar dados."}, 500