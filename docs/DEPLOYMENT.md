# Guia de Deploy - Nurgling Cookbook Pro

Este documento fornece instruções detalhadas para deploy da aplicação em diferentes ambientes.

## 📋 Pré-requisitos

Antes de fazer o deploy, certifique-se de que:

- [ ] O banco de dados foi criado (`python scripts/setup_database.py`)
- [ ] O arquivo `.env` foi configurado corretamente
- [ ] A `SECRET_KEY` foi gerada e configurada
- [ ] As dependências foram instaladas (`pip install -r requirements.txt`)
- [ ] Os logs de teste foram verificados

## 🌐 Deploy em Servidor Linux (VPS/Cloud)

### Opção 1: Deploy com Systemd (Recomendado)

Ideal para servidores Linux tradicionais (Ubuntu, Debian, CentOS).

#### Passo 1: Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e dependências
sudo apt install -y python3.11 python3-pip python3-venv nginx

# Criar usuário para a aplicação
sudo useradd -m -s /bin/bash nurgling
sudo usermod -aG www-data nurgling
```

#### Passo 2: Configurar a Aplicação

```bash
# Copiar arquivos para o servidor
scp -r nurgling-cookbook-pro/ user@server:/home/nurgling/

# Conectar ao servidor
ssh user@server

# Mudar para o diretório
cd /home/nurgling/nurgling-cookbook-pro

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env  # Editar configurações

# Ajustar permissões
sudo chown -R nurgling:www-data /home/nurgling/nurgling-cookbook-pro
sudo chmod 755 /home/nurgling/nurgling-cookbook-pro
```

#### Passo 3: Criar Serviço Systemd

```bash
sudo nano /etc/systemd/system/nurgling-cookbook-pro.service
```

Conteúdo do arquivo:

```ini
[Unit]
Description=Nurgling Cookbook Pro
After=network.target

[Service]
Type=notify
User=nurgling
Group=www-data
WorkingDirectory=/home/nurgling/nurgling-cookbook-pro
Environment="PATH=/home/nurgling/nurgling-cookbook-pro/venv/bin"
EnvironmentFile=/home/nurgling/nurgling-cookbook-pro/.env
ExecStart=/home/nurgling/nurgling-cookbook-pro/venv/bin/gunicorn --config gunicorn.conf.py wsgi:app
Restart=always
RestartSec=10
StandardOutput=append:/home/nurgling/nurgling-cookbook-pro/logs/app.log
StandardError=append:/home/nurgling/nurgling-cookbook-pro/logs/error.log

[Install]
WantedBy=multi-user.target
```

#### Passo 4: Iniciar Serviço

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar serviço
sudo systemctl enable nurgling-cookbook-pro

# Iniciar serviço
sudo systemctl start nurgling-cookbook-pro

# Verificar status
sudo systemctl status nurgling-cookbook-pro

# Ver logs
sudo journalctl -u nurgling-cookbook-pro -f
```

#### Passo 5: Configurar Nginx (Proxy Reverso)

```bash
sudo nano /etc/nginx/sites-available/nurgling-cookbook-pro
```

Conteúdo:

```nginx
server {
    listen 80;
    server_name seu-dominio.com;  # Altere para seu domínio

    # Logs
    access_log /var/log/nginx/nurgling-access.log;
    error_log /var/log/nginx/nurgling-error.log;

    # Proxy para Gunicorn
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
}
```

Ativar site:

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/nurgling-cookbook-pro /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

#### Passo 6: Configurar SSL (Opcional mas Recomendado)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática já está configurada
```

### Opção 2: Deploy com Docker

Ideal para ambientes containerizados.

#### Passo 1: Instalar Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install -y docker-compose
```

#### Passo 2: Preparar Arquivos

```bash
# Copiar projeto para servidor
scp -r nurgling-cookbook-pro/ user@server:/opt/

# Conectar ao servidor
ssh user@server
cd /opt/nurgling-cookbook-pro

# Configurar .env
cp .env.example .env
nano .env
```

#### Passo 3: Build e Deploy

```bash
# Build da imagem
docker build -t nurgling-cookbook-pro:latest .

# Executar container
docker run -d \
    --name nurgling-cookbook-pro \
    --restart unless-stopped \
    -p 5000:5000 \
    -v $(pwd)/nurglingdatabase.db:/app/nurglingdatabase.db:ro \
    -v $(pwd)/logs:/app/logs \
    --env-file .env \
    nurgling-cookbook-pro:latest

# Verificar logs
docker logs -f nurgling-cookbook-pro
```

Ou com Docker Compose:

```bash
docker-compose up -d --build
docker-compose logs -f
```

## ☁️ Deploy em Cloud Providers

### AWS (EC2 + RDS)

1. **Criar instância EC2**
   - Ubuntu 22.04 LTS
   - t2.small ou superior
   - Abrir portas 80 e 443

2. **Seguir passos do deploy com Systemd**

3. **Configurar RDS** (opcional, para PostgreSQL)
   - Criar instância RDS PostgreSQL
   - Atualizar `config.py` para usar PostgreSQL
   - Instalar `psycopg2-binary`

### Google Cloud Platform (App Engine)

Criar `app.yaml`:

```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT wsgi:app

env_variables:
  FLASK_ENV: production
  SECRET_KEY: "sua-secret-key"
  
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

Deploy:

```bash
gcloud app deploy
```

### Heroku

```bash
# Login
heroku login

# Criar app
heroku create nurgling-cookbook-pro

# Adicionar Procfile
echo "web: gunicorn --config gunicorn.conf.py wsgi:app" > Procfile

# Configurar variáveis
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Deploy
git push heroku main

# Ver logs
heroku logs --tail
```

### DigitalOcean (App Platform)

1. Conectar repositório GitHub
2. Configurar:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --config gunicorn.conf.py wsgi:app`
3. Adicionar variáveis de ambiente
4. Deploy

## 🔄 Atualizações e Manutenção

### Atualizar Aplicação (Systemd)

```bash
# Conectar ao servidor
ssh user@server
cd /home/nurgling/nurgling-cookbook-pro

# Ativar ambiente virtual
source venv/bin/activate

# Puxar atualizações
git pull origin main

# Instalar novas dependências (se houver)
pip install -r requirements.txt

# Reiniciar serviço
sudo systemctl restart nurgling-cookbook-pro

# Verificar status
sudo systemctl status nurgling-cookbook-pro
```

### Atualizar Aplicação (Docker)

```bash
# Puxar atualizações
git pull origin main

# Rebuild e restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Ou com Docker direto
docker stop nurgling-cookbook-pro
docker rm nurgling-cookbook-pro
docker build -t nurgling-cookbook-pro:latest .
docker run -d ... (mesmo comando anterior)
```

### Backup do Banco de Dados

```bash
# Criar backup
cp nurglingdatabase.db nurglingdatabase.db.backup.$(date +%Y%m%d)

# Ou com script automatizado
cat > /home/nurgling/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/nurgling/backups"
mkdir -p $BACKUP_DIR
cp /home/nurgling/nurgling-cookbook-pro/nurglingdatabase.db \
   $BACKUP_DIR/nurglingdatabase.db.$(date +%Y%m%d_%H%M%S)
# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.db.*" -mtime +7 -delete
EOF

chmod +x /home/nurgling/backup.sh

# Adicionar ao crontab
crontab -e
# Adicionar: 0 2 * * * /home/nurgling/backup.sh
```

## 📊 Monitoramento

### Logs

```bash
# Systemd
sudo journalctl -u nurgling-cookbook-pro -f

# Docker
docker logs -f nurgling-cookbook-pro

# Arquivos de log
tail -f logs/app.log
tail -f logs/error.log
tail -f logs/access.log
```

### Health Check

```bash
# Verificar se aplicação está respondendo
curl http://localhost:5000/health

# Verificar estatísticas
curl http://localhost:5000/api/stats
```

### Monitoramento com Prometheus (Opcional)

Instalar `prometheus-flask-exporter`:

```bash
pip install prometheus-flask-exporter
```

Adicionar ao `app/__init__.py`:

```python
from prometheus_flask_exporter import PrometheusMetrics

def create_app(config_name=None):
    app = Flask(__name__)
    # ... configurações existentes ...
    
    # Adicionar métricas
    metrics = PrometheusMetrics(app)
    
    return app
```

## 🚨 Troubleshooting

### Serviço não inicia

```bash
# Ver logs detalhados
sudo journalctl -u nurgling-cookbook-pro -n 100 --no-pager

# Verificar permissões
ls -la /home/nurgling/nurgling-cookbook-pro

# Testar manualmente
cd /home/nurgling/nurgling-cookbook-pro
source venv/bin/activate
python wsgi.py
```

### Erro 502 Bad Gateway (Nginx)

```bash
# Verificar se Gunicorn está rodando
sudo systemctl status nurgling-cookbook-pro

# Verificar se porta está aberta
sudo netstat -tlnp | grep 5000

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

### Alto uso de memória

```bash
# Reduzir número de workers no .env
WORKERS=2

# Ou no gunicorn.conf.py
workers = 2

# Reiniciar
sudo systemctl restart nurgling-cookbook-pro
```

## 🔒 Checklist de Segurança

Antes de ir para produção:

- [ ] SECRET_KEY gerada aleatoriamente
- [ ] DEBUG=False em produção
- [ ] Firewall configurado (apenas portas 80, 443, 22)
- [ ] SSL/TLS configurado
- [ ] Banco de dados com permissões restritas
- [ ] Rate limiting habilitado
- [ ] Logs configurados
- [ ] Backups automatizados
- [ ] Monitoramento ativo
- [ ] Atualizações de segurança do sistema

---

**Última atualização:** Dezembro 2025
