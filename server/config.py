from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class DevConfig(Config):
    # FLASK_ENV = 'development' 
    ENV = 'development'
    TESTING = True
    DEBUG = True

class ProdConfig(Config):
    ENV = 'production'
    TESTING = False
    DEBUG = False