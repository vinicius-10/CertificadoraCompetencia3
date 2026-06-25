from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db
from flask_login import current_user
from app.utils import parse_from_date


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
    if not User.email_validate(email):
        return {"success": False, "message": "Email inválido."}, 400
    
    # validar rg
    if not User.rg_validate(rg):
        return {"success": False, "message": "RG inválido."}, 400
    
    # validar profissão
    if not profession.replace(" ","").isalpha() or len(profession) > 100:
        return {"success": False, "message": "A profissão deve conter apenas letras."}, 400
    
    #validar estado civil
    if not (marital in [UserMarital.SINGLE.name, UserMarital.MARRIED.name, UserMarital.DIVORCED.name, UserMarital.WIDOWED.name, UserMarital.STABLE_UNION.name]):
        return {"success": False, "message": "Estado civil inválido."}, 400
    
    #validar nacionalidade
    if not nationality.replace(" ","").isalpha() or len(nationality) > 50:
        return {"success": False, "message": "A nacionalidade deve conter apenas letras e ser menor que 50 caracteres."}, 400
    
    #validar RA
    if not code_institutional.isdigit() or len(code_institutional) > 20:
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
    if not complement.replace(" ","").isalnum() or len(complement) > 100:
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
    
    #validar data de entrada
    data_entry = parse_from_date(entry_at)
    
    if not data_entry:
        return {"success": False, "message": "Data de entrada inválida."}, 400
    
    #validar data de saída
    data_departure = parse_from_date(departure_at)
    # mudar a lógica para permitir que a data de sáida seja none
    if not data_departure or data_departure < data_entry:
        return {"success": False, "message": "Data de saída inválida."}, 400
    
    #inserção no BD
    
    try:
        user1 = User(
            code_institutional= code_institutional,
            name= username,
            email= email,
            cpf= cpf,
            rg= rg,
            nationality= nationality,
            marital= UserMarital[marital],
            profession= profession,
            profile= UserProfile[profile],
            status= UserStatus[status],
            sector= UserSector[sector],
            position= UserPosition[position],
            entry_at= data_entry,
        )

        # Criando e vinculando o endereço diretamente
        addr1 = Address(
            postal_code= postal_code,
            street= street,
            number= number,
            complement= complement,
            neighborhood= neighborhood,
            city= city,
            state= state,
            country= country,
            user=user1 # O SQLAlchemy vincula o ID automaticamente aqui
        )
        
        db.session.add_all([user1, addr1])
        db.session.commit()
        return {"success": True, "message": "Usuário Registrado com Sucesso."}, 201
    except:
        db.session.rollback()
        return {"success": False, "message": "Erro ao registrar usuário."}, 500