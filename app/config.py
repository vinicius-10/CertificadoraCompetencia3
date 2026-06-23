
from datetime import timedelta
from os import environ

class Config:
    #valores para bloquear usuario após tentativas de login
    MAX_LOGIN_ATTEMPTS = 5
    WITHIN_MINUTES = 5
    MINUTES_BLOCKED = 15
    
    # Chaves de segurança e Banco de Dados
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações de Sessão e Cookies
    SESSION_COOKIE_DURATION = timedelta(hours=8)
    SESSION_COOKIE_LIFETIME = timedelta(hours=8)
    SESSION_COOKIE_HTTPONLY = True
    
    # Se FLASK_ENV for 'development', SECURE será False. Caso contrário (produção), True.
    SESSION_COOKIE_SECURE = environ.get('FLASK_ENV') != 'development'
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    #email
    
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = environ.get('MAIL_PORT')
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_TIMEOUT = int(environ.get('MAIL_TIMEOUT'))
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')