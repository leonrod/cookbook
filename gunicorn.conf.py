"""
Configuração do Gunicorn para produção
"""
import os
import multiprocessing

# Bind
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"

# Workers
workers = int(os.environ.get('WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gevent'
worker_connections = 1000

# Timeouts
timeout = 30
keepalive = 2

# Logging
accesslog = os.environ.get('ACCESS_LOG', 'logs/access.log')
errorlog = os.environ.get('ERROR_LOG', 'logs/error.log')
loglevel = os.environ.get('LOG_LEVEL', 'info').lower()

# Process naming
proc_name = 'nurgling-cookbook-pro'

# Server mechanics
daemon = False
pidfile = 'logs/gunicorn.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (se necessário)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# Preload app para economizar memória
preload_app = True

# Restart workers periodicamente para evitar memory leaks
max_requests = 1000
max_requests_jitter = 50

def on_starting(server):
    """Executado quando o servidor inicia"""
    server.log.info("Gunicorn server starting...")

def on_reload(server):
    """Executado quando o servidor recarrega"""
    server.log.info("Gunicorn server reloading...")

def when_ready(server):
    """Executado quando o servidor está pronto"""
    server.log.info("Gunicorn server ready. Listening on: %s", bind)

def on_exit(server):
    """Executado quando o servidor encerra"""
    server.log.info("Gunicorn server shutting down...")
