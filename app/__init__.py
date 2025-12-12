"""
Inicialização da aplicação Flask
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

from app.config import get_config
from app.database import init_db_connection, verificar_integridade_db


# Instâncias de extensões
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

cache = Cache()


def create_app(config_name=None):
    """
    Factory function para criar a aplicação Flask.
    
    Args:
        config_name: Nome da configuração a usar (development, production, testing)
        
    Returns:
        Instância configurada da aplicação Flask
    """
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    
    # Carregar configuração
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Forçar reload de templates
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    
    # Criar diretório de logs se não existir
    log_dir = Path(app.config['LOG_FILE']).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Configurar logging
    setup_logging(app)
    
    # Verificar integridade do banco de dados
    if not app.config['TESTING']:
        sucesso, mensagem = verificar_integridade_db(app.config['DB_PATH'])
        if not sucesso:
            app.logger.error(f"Database integrity check failed: {mensagem}")
            raise RuntimeError(f"Database error: {mensagem}")
        app.logger.info(f"Database integrity check: {mensagem}")
    
    # Inicializar extensões
    init_extensions(app)
    
    # Inicializar conexão de banco de dados
    init_db_connection(app)
    
    # Registrar blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    # Log de inicialização
    app.logger.info(f"Application started in {config_name or 'default'} mode")
    
    return app


def setup_logging(app):
    """
    Configura o sistema de logging da aplicação.
    
    Args:
        app: Instância da aplicação Flask
    """
    if not app.debug and not app.testing:
        # Handler para arquivo
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'],
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        app.logger.addHandler(file_handler)
    
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info('Nurgling Cookbook Pro startup')


def init_extensions(app):
    """
    Inicializa as extensões Flask.
    
    Args:
        app: Instância da aplicação Flask
    """
    # CORS
    if app.config.get('CORS_ENABLED'):
        CORS(app, origins=app.config.get('CORS_ORIGINS'))
        app.logger.info(f"CORS enabled for origins: {app.config.get('CORS_ORIGINS')}")
    
    # Rate Limiting
    if app.config.get('RATELIMIT_ENABLED'):
        limiter.init_app(app)
        app.logger.info(f"Rate limiting enabled: {app.config.get('RATELIMIT_DEFAULT')}")
    
    # Cache
    cache.init_app(app, config={
        'CACHE_TYPE': app.config.get('CACHE_TYPE'),
        'CACHE_DEFAULT_TIMEOUT': app.config.get('CACHE_DEFAULT_TIMEOUT')
    })
    app.logger.info(f"Cache initialized: {app.config.get('CACHE_TYPE')}")
