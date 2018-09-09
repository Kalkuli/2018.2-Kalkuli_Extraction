class BaseConfig:
    """Base configuration"""
    TESTING = False

class DevConfig(BaseConfig):
    pass

class TestingConfig(BaseConfig):
    TESTING = True

class ProductionConfig(BaseConfig):
    pass