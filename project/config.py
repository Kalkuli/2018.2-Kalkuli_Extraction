import os


class BaseConfig:
    TESTING = False

class DevelopmentConfig(BaseConfig):
    THIS = 'Development'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')

class TestingConfig(BaseConfig):
    TESTING = True
    THIS = 'Testing'

class ProductionConfig(BaseConfig):
    THIS = 'Production'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')