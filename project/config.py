class BaseConfig:
    TESTING = False

class DevelopmentConfig(BaseConfig):
    THIS = 'Development'

class TestingConfig(BaseConfig):
    TESTING = True
    THIS = 'Testing'

class ProductionConfig(BaseConfig):
    THIS = 'Production'