import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # TODO: Change this during deployment
    SECRET_KEY = 'E943zmOeGh8P-FHM-u0O9g'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
