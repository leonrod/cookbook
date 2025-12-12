#!/bin/bash
#
# Script de deploy para Nurgling Cookbook Pro
#

set -e  # Sair em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Nurgling Cookbook Pro - Deploy${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "wsgi.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    echo -e "${YELLOW}   Copiando .env.example para .env...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}   ⚠️  IMPORTANTE: Edite o arquivo .env antes de continuar!${NC}"
    exit 1
fi

# Verificar SECRET_KEY
if grep -q "your-secret-key-here" .env; then
    echo -e "${RED}❌ Erro: SECRET_KEY não foi configurada no arquivo .env${NC}"
    echo -e "${YELLOW}   Gere uma chave com: python -c \"import secrets; print(secrets.token_hex(32))\"${NC}"
    exit 1
fi

# Verificar se banco de dados existe
if [ ! -f "nurglingdatabase.db" ]; then
    echo -e "${YELLOW}⚠️  Banco de dados não encontrado${NC}"
    echo -e "${YELLOW}   Execute: python scripts/setup_database.py${NC}"
    exit 1
fi

# Carregar variáveis de ambiente
export $(cat .env | grep -v '^#' | xargs)

# Determinar modo de deploy
DEPLOY_MODE=${1:-"local"}

case $DEPLOY_MODE in
    "local")
        echo -e "${GREEN}📦 Deploy Local (Gunicorn)${NC}"
        echo ""
        
        # Instalar dependências
        echo "📥 Instalando dependências..."
        pip install -q -r requirements.txt
        
        # Criar diretórios necessários
        mkdir -p logs
        
        # Verificar integridade do banco
        echo "🔍 Verificando banco de dados..."
        python -c "from app.database import verificar_integridade_db; import sys; ok, msg = verificar_integridade_db('nurglingdatabase.db'); print(msg); sys.exit(0 if ok else 1)"
        
        # Iniciar servidor
        echo ""
        echo -e "${GREEN}🚀 Iniciando servidor...${NC}"
        echo -e "${YELLOW}   Acesse: http://localhost:${PORT:-5000}${NC}"
        echo ""
        gunicorn --config gunicorn.conf.py wsgi:app
        ;;
        
    "docker")
        echo -e "${GREEN}🐳 Deploy com Docker${NC}"
        echo ""
        
        # Verificar se Docker está instalado
        if ! command -v docker &> /dev/null; then
            echo -e "${RED}❌ Docker não está instalado${NC}"
            exit 1
        fi
        
        # Build da imagem
        echo "🔨 Construindo imagem Docker..."
        docker build -t nurgling-cookbook-pro:latest .
        
        # Parar container existente (se houver)
        echo "🛑 Parando container existente..."
        docker stop nurgling-cookbook-pro 2>/dev/null || true
        docker rm nurgling-cookbook-pro 2>/dev/null || true
        
        # Iniciar novo container
        echo "🚀 Iniciando container..."
        docker run -d \
            --name nurgling-cookbook-pro \
            --restart unless-stopped \
            -p ${PORT:-5000}:5000 \
            -v $(pwd)/nurglingdatabase.db:/app/nurglingdatabase.db:ro \
            -v $(pwd)/logs:/app/logs \
            --env-file .env \
            nurgling-cookbook-pro:latest
        
        echo ""
        echo -e "${GREEN}✅ Container iniciado com sucesso!${NC}"
        echo -e "${YELLOW}   Acesse: http://localhost:${PORT:-5000}${NC}"
        echo -e "${YELLOW}   Logs: docker logs -f nurgling-cookbook-pro${NC}"
        ;;
        
    "docker-compose")
        echo -e "${GREEN}🐳 Deploy com Docker Compose${NC}"
        echo ""
        
        # Verificar se Docker Compose está instalado
        if ! command -v docker-compose &> /dev/null; then
            echo -e "${RED}❌ Docker Compose não está instalado${NC}"
            exit 1
        fi
        
        # Build e start
        echo "🔨 Construindo e iniciando serviços..."
        docker-compose up -d --build
        
        echo ""
        echo -e "${GREEN}✅ Serviços iniciados com sucesso!${NC}"
        echo -e "${YELLOW}   Acesse: http://localhost:${PORT:-5000}${NC}"
        echo -e "${YELLOW}   Logs: docker-compose logs -f${NC}"
        echo -e "${YELLOW}   Parar: docker-compose down${NC}"
        ;;
        
    "systemd")
        echo -e "${GREEN}⚙️  Deploy com Systemd${NC}"
        echo ""
        
        # Criar arquivo de serviço
        SERVICE_FILE="/etc/systemd/system/nurgling-cookbook-pro.service"
        
        echo "📝 Criando arquivo de serviço..."
        sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Nurgling Cookbook Pro
After=network.target

[Service]
Type=notify
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
EnvironmentFile=$(pwd)/.env
ExecStart=$(which gunicorn) --config gunicorn.conf.py wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

        # Recarregar systemd
        echo "🔄 Recarregando systemd..."
        sudo systemctl daemon-reload
        
        # Habilitar e iniciar serviço
        echo "🚀 Iniciando serviço..."
        sudo systemctl enable nurgling-cookbook-pro
        sudo systemctl restart nurgling-cookbook-pro
        
        echo ""
        echo -e "${GREEN}✅ Serviço instalado e iniciado!${NC}"
        echo -e "${YELLOW}   Status: sudo systemctl status nurgling-cookbook-pro${NC}"
        echo -e "${YELLOW}   Logs: sudo journalctl -u nurgling-cookbook-pro -f${NC}"
        echo -e "${YELLOW}   Parar: sudo systemctl stop nurgling-cookbook-pro${NC}"
        ;;
        
    *)
        echo -e "${RED}❌ Modo de deploy inválido: $DEPLOY_MODE${NC}"
        echo ""
        echo "Uso: $0 [local|docker|docker-compose|systemd]"
        echo ""
        echo "Modos disponíveis:"
        echo "  local          - Deploy local com Gunicorn"
        echo "  docker         - Deploy em container Docker"
        echo "  docker-compose - Deploy com Docker Compose"
        echo "  systemd        - Deploy como serviço systemd"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Deploy concluído com sucesso! 🎉${NC}"
echo -e "${GREEN}========================================${NC}"
