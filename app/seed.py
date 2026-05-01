from models import db, User, UserProfile, UserStatus, UserMarital

def seed_data():
    
    if not User.query.first():
        
        new_user = User(
            ra="00000",
            name="João Silva",
            email="email@example.com",
            cpf="123.456.789-00",
            rg="12.345.678-9",
            nationality='Brasileiro',
            marital=UserMarital.SINGLE,
            profession='Teste',
            profile=UserProfile.ADMIN,
            status=UserStatus.ACTIVE
        )
        
        new_user.set_password("senha")
        
        db.session.add(new_user)
        db.session.commit()
        
        print("Dados de semente (seed) inseridos com sucesso!")
    else:
        print("Dados de semente já existem. Pulando...")