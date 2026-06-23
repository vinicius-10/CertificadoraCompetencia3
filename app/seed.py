from app.models import db, User, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address
from datetime import datetime, timezone

def seed_data():
    print("Iniciando inserção de dados de semente (seed)...")
    if not User.query.first():
        
        user1 = User(
            code_institutional="99001",
            name="Coordenação Geral",
            email="meninasdigitaishub@gmail.com",
            cpf="69545514060",       # CPF Válido para testes
            rg="432314545",          # RG fictício estruturado
            nationality="Brasileira",
            marital=UserMarital.MARRIED,
            profession="Administrador",
            profile=UserProfile.COORDINATOR,
            status=UserStatus.ACTIVE,
            sector=UserSector.RH,
            position=UserPosition.STUDANT_COORDINATOR,
            entry_at=datetime.now(timezone.utc),
        )
        user1.set_password("admin123")

        # Criando e vinculando o endereço diretamente
        addr1 = Address(
            postal_code="01001000",
            street="Praça da Sé",
            number="123",
            complement="Bloco A",
            neighborhood="Sé",
            city="São Paulo",
            state="SP",
            country="Brasil",
            user=user1 # O SQLAlchemy vincula o ID automaticamente aqui
        )
        
        user2 = User(
            code_institutional="99002",
            name="Ana Silva (Bolsista)",
            email="vinicius.2023@alunos.utfpr.edu.br",
            cpf="88504051030",       # CPF Válido para testes
            rg="112223334",
            nationality="Brasileira",
            marital=UserMarital.SINGLE,
            profession="Estudante",
            profile=UserProfile.SCHOLARSHIP,
            status=UserStatus.ACTIVE,
            sector=UserSector.CONTENT,
            position=UserPosition.REPRESENTATIVE,
            entry_at=datetime.now(timezone.utc),
        )
       
        user2.set_password("bolsista123")

        addr2 = Address(
            postal_code="20040002",
            street="Avenida Rio Branco",
            number="500",
            complement="Apto 402",
            neighborhood="Centro",
            city="Rio de Janeiro",
            state="RJ",
            country="Brasil",
            user=user2
        )

        # --- USUÁRIO 3: VOLUNTÁRIO ---
        user3 = User(
            code_institutional="99003",
            name="Carlos Souza (Voluntário)",
            email="vs211570@gmail.com",
            cpf="17500198094",       # CPF Válido para testes
            rg="998887776",
            nationality="Brasileira",
            marital=UserMarital.STABLE_UNION,
            profession="Desenvolvedor",
            profile=UserProfile.VOLUNTEER, # Ajustado para bater com seu Enum (VOLUNTEER ou VOLUNTARY)
            status=UserStatus.ACTIVE,
            sector=UserSector.MARKETING,
            position=UserPosition.VOLUNTEER,
            entry_at=datetime.now(timezone.utc),
        )
        user3.set_password("voluntario123")

        addr3 = Address(
            postal_code="30140010",
            street="Rua dos Guajajaras",
            number="1000",
            complement=None,
            neighborhood="Lourdes",
            city="Belo Horizonte",
            state="MG",
            country="Brasil",
            user=user3
        )

        # Adiciona tudo na sessão e commita de uma vez
        db.session.add_all([user1, addr1, user2, addr2, user3, addr3])
        db.session.commit()
        
        print("Dados de semente (seed) inseridos com sucesso!")
    else:
        print("Dados de semente já existem. Pulando...")