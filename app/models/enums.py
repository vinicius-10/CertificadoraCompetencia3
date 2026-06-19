from enum import Enum



class UserProfile(Enum):
    COORDINATOR  = "Coordenador(a)"
    SCHOLARSHIP  = "Bolsista"
    VOLUNTEER  = "Voluntário(a)"

class UserStatus(Enum):
    ACTIVE = "Ativo"
    INACTIVE = "Desligado"
    DELETED = "Excluído"

class UserMarital(Enum):
    SINGLE  = "Solteiro(a)"
    MARRIED  = "Casado(a)"
    DIVORCED  = "Divorciado(a)"
    WIDOWED  = "Viúvo(a)"
    STABLE_UNION = "União Estável"     
    
class UserSector(Enum):
    MARKETING = "Marketing"
    RH = "Recursos Humanos"
    CONTENT = "Conteúdo"
    INSTRUCTORS = "Instrutor"
    
class UserPosition(Enum):
    STUDANT_COORDINATOR = "Coordenador(a) estudantil"
    REPRESENTATIVE = "Representante do setor"
    VOLUNTEER = "Voluntário(a)"