import os
from pthemes import app

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-is-not-a-secret'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DATABASE = os.path.join(app.root_path, 'pthemes.db')

class TestingConfig(Config):
    TESTING = True