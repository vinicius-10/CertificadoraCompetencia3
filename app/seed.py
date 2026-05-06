from models import db, User, UserProfile, UserStatus, UserMarital

def seed_data():
    
    if not User.query.first():
        
        new_user = User(
            code_institutional="00000",
            name="admin",
            email="email@example.com",
            cpf="11111111111",
            rg="111111111",
            nationality='Brasileiro',
            marital=UserMarital.SINGLE,
            profession='Teste',
            profile=UserProfile.ADMIN,
            status=UserStatus.ACTIVE,
        )
        
        new_user.set_password("senha")
        
        db.session.add(new_user)
        db.session.commit()
        
        new_user = User(
            code_institutional="00002",
            name="user",
            email="email2@example.com",
            cpf="22222222222",
            rg="222222222",
            nationality='Brasileiro',
            marital=UserMarital.SINGLE,
            profession='Teste',
            profile=UserProfile.VOLUNTEER,
            status=UserStatus.ACTIVE,
        )
        
        new_user.set_password("senha")
        
        db.session.add(new_user)
        db.session.commit()
        
        print("Dados de semente (seed) inseridos com sucesso!")
    else:
        print("Dados de semente já existem. Pulando...")