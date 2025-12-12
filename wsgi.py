"""
WSGI entry point para deploy em produção
"""
import os
from app import create_app

# Determinar ambiente
env = os.environ.get('FLASK_ENV', 'production')

# Criar aplicação
app = create_app(env)

if __name__ == '__main__':
    # Para desenvolvimento local
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
