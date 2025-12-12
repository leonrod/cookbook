"""
Configurações da aplicação Nurgling Cookbook Pro
"""
import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Configuração base"""
    # Segurança
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Banco de dados
    DB_PATH = os.environ.get('DB_PATH') or str(BASE_DIR / 'nurglingdatabase.db')
    
    # API
    API_RESULTS_LIMIT = int(os.environ.get('API_RESULTS_LIMIT', 50))
    API_MAX_QUERY_LENGTH = int(os.environ.get('API_MAX_QUERY_LENGTH', 500))
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE') or str(BASE_DIR / 'logs' / 'app.log')
    
    # CORS
    CORS_ENABLED = os.environ.get('CORS_ENABLED', 'False').lower() == 'true'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # Rate Limiting
    RATELIMIT_ENABLED = os.environ.get('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '100 per minute')
    
    # Cache
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))


class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    TESTING = False
    
    # Em produção, SECRET_KEY deve ser obrigatória
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable must be set in production")


class TestingConfig(Config):
    """Configuração de testes"""
    DEBUG = True
    TESTING = True
    DB_PATH = ':memory:'  # Banco em memória para testes


# Mapeamento de ambientes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """Retorna a configuração apropriada baseada no ambiente"""
    if env_name is None:
        env_name = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env_name, DevelopmentConfig)
