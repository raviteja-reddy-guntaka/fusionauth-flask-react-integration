import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    FUSIONAUTH_URL = os.getenv('FUSIONAUTH_URL')
    FUSIONAUTH_CLIENT_ID = os.getenv('FUSIONAUTH_CLIENT_ID')
    FUSIONAUTH_CLIENT_SECRET = os.getenv('FUSIONAUTH_CLIENT_SECRET')
    FUSIONAUTH_REDIRECT_URI = os.getenv('FUSIONAUTH_REDIRECT_URI')
    
    # Cookie settings
    COOKIE_NAME = 'auth_token'
    COOKIE_HTTPONLY = True
    COOKIE_SECURE = os.getenv('COOKIE_SECURE', 'False').lower() == 'true'
    COOKIE_SAMESITE = os.getenv('COOKIE_SAMESITE', 'Lax')
    COOKIE_DOMAIN = os.getenv('COOKIE_DOMAIN', 'localhost')
    
    # CORS
    CORS_ORIGINS = os.getenv('FRONTEND_URL', 'http://localhost:3000').split(',')

class DevelopmentConfig(Config):
    DEBUG = True
    FRONTEND_URL = 'http://localhost:3000'

class ProductionConfig(Config):
    DEBUG = False
    COOKIE_SECURE = True
    COOKIE_SAMESITE = 'None'  # For cross-site cookies
