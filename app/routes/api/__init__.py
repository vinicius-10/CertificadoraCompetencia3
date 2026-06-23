from flask import Blueprint

from app.routes.api.auth_api import auth_api_bp
from app.routes.api.user_api import user_api_bp


api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_api_bp, url_prefix='/auth')

api_bp.register_blueprint(user_api_bp, url_prefix='/user')

