# app/models/__init__.py

#docker-compose exec web flask db migrate -m "descricao"
#docker-compose exec web flask db upgrade


from app.models.db_instance import db

# 1. Importe ABSOLUTAMENTE TODOS os seus modelos aqui
from app.models.user import User
from app.models.address import Address
from app.models.status_history import StatusHistory
from app.models.access_log import AccessLog
from app.models.password_recovery import PasswordRecoveryToken
from app.models.user_block import UserBlock
from app.models.enums import UserProfile, UserStatus, UserMarital, UserSector, UserPosition

# 2. Exponha todos eles para o resto do app
__all__ = [
    'db', 
    'User', 
    'Address', 
    'StatusHistory', 
    'AccessLog', 
    'PasswordRecoveryToken', 
    'UserBlock',
    'UserProfile',
    'UserStatus',
    'UserMarital',
    'UserSector',
    'UserPosition'
]