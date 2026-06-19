from enum import Enum



class UserProfile(Enum):
    COORDINATOR  = "Coordenador(a)"
    ADMIN  = "Admin"
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
    
