from app.models import User, UserBlock, UserProfile, UserStatus, UserMarital, UserSector, UserPosition, Address, db
from flask_login import current_user
from app.utils import parse_from_date

def update_user_from_user(data):
    
    usuário = current_user.id