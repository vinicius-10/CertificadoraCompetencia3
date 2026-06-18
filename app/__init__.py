import os
from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from app.models import db, User
from app.seed import seed_data


migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    _configure_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    _configure_login_manager(app)

    _register_blueprints(app)

    @app.cli.command("seed-db")
    def seed_db_command():
        seed_data()

    return app

def _configure_app(app):
    env = os.environ
    app.config['SQLALCHEMY_DATABASE_URI'] = env.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = env.get('SECRET_KEY')
    app.config['SESSION_COOKIE_DURATION'] = timedelta(hours=8)
    app.config['SESSION_COOKIE_LIFETIME'] = timedelta(hours=8)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = False if (env.get('FLASK_ENV') == 'development') else True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

def _configure_login_manager(app):
    login_manager.login_view = 'main.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

def _register_blueprints(app):
    
    from app.main_routes import main_bp
    from app.test_routes import test_bp
    from app.api_routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp, url_prefix="/test")
    app.register_blueprint(api_bp, url_prefix="/api")