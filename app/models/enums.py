from enum import Enum



class UserProfile(Enum):
    COORDINATOR  = "Coordenador(a)"
    SCHOLARSHIP  = "Bolsista"
    VOLUNTEER  = "Voluntário(a)"
    
    @classmethod
    def from_string(cls, value: str):
        if not value:
            return None
        try:
            return cls[value]
        except:
            return None

class UserStatus(Enum):
    ACTIVE = "Ativo"
    INACTIVE = "Desligado"
    DELETED = "Excluído"
    
    @classmethod
    def from_string(cls, value: str):
        if not value:
            return None
        try:
            return cls[value]
        except:
            return None

class UserMarital(Enum):
    SINGLE  = "Solteiro(a)"
    MARRIED  = "Casado(a)"
    DIVORCED  = "Divorciado(a)"
    WIDOWED  = "Viúvo(a)"
    STABLE_UNION = "União Estável"
    
    @classmethod
    def from_string(cls, value: str):
        if not value:
            return None
        try:
            return cls[value]
        except:
            return None
    
class UserSector(Enum):
    MARKETING = "Marketing"
    RH = "Recursos Humanos"
    CONTENT = "Conteúdo"
    INSTRUCTORS = "Instrutor"
    
    @classmethod
    def from_string(cls, value: str):
        if not value:
            return None
        try:
            return cls[value]
        except:
            return None
    
class UserPosition(Enum):
    STUDANT_COORDINATOR = "Coordenador(a) estudantil"
    REPRESENTATIVE = "Representante do setor"
    VOLUNTEER = "Voluntário(a)"
    
    @classmethod
    def from_string(cls, value: str):
        if not value:
            return None
        try:
            return cls[value]
        except:
            return None