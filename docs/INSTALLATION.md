# Guia de Instalação - AgentHub

## 📋 Pré-requisitos

### Software Necessário
- **Docker Desktop** (Windows/Mac) ou **Docker Engine** (Linux)
- **Docker Compose** v2.0+
- **Node.js** 18+ e **npm**
- **Git** para clonar o repositório

### Contas de Serviços Externos
- **OpenAI API Key** (para funcionalidade de IA)
- **Conta GitHub** (opcional, para desenvolvimento)

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/agenthub.git
cd agenthub
```

### 2. Configurar Variáveis de Ambiente
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
nano .env  # ou use seu editor preferido
```

**Configurações obrigatórias no .env:**
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
SECRET_KEY=your-secure-secret-key-minimum-32-characters
```

### 3. Iniciar Backend (Microsserviços)

**No Windows (PowerShell):**
```powershell
.\scripts\start-dev.ps1
```

**No Linux/Mac:**
```bash
chmod +x scripts/start-dev.sh
./scripts/start-dev.sh
```

**Ou manualmente:**
```bash
cd backend/docker
docker-compose up -d
```

### 4. Instalar e Iniciar Frontend
```bash
# Instalar dependências
npm install

# Iniciar em modo desenvolvimento
npm run dev
```

### 5. Acessar a Plataforma
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:80
- **MinIO Console**: http://localhost:9001 (admin/minioadmin)

## 🔧 Instalação Detalhada

### Configuração do Docker

#### Windows
1. Baixe e instale o Docker Desktop
2. Habilite WSL2 se estiver no Windows 10/11
3. Reinicie o computador se necessário

#### Linux (Ubuntu/Debian)
```bash
# Atualizar pacotes
sudo apt update

# Instalar Docker
sudo apt install docker.io docker-compose

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Reiniciar sessão
newgrp docker
```

#### macOS
1. Baixe e instale o Docker Desktop para Mac
2. Inicie o Docker Desktop
3. Verifique se está rodando: `docker --version`

### Configuração do Banco de Dados

Os bancos de dados PostgreSQL são criados automaticamente via Docker. Se precisar configurar manualmente:

```bash
# Conectar ao PostgreSQL
docker exec -it agenthub-postgres-auth psql -U agenthub -d auth_service

# Executar scripts de criação
\i /docker-entrypoint-initdb.d/init.sql
```

### Configuração do MinIO

O MinIO é configurado automaticamente, mas você pode acessar o console:

1. Acesse http://localhost:9001
2. Login: `minioadmin`
3. Senha: `minioadmin`
4. Criar bucket `documents` se não existir

### Configuração do Redis

O Redis é iniciado automaticamente. Para verificar:

```bash
# Conectar ao Redis
docker exec -it agenthub-redis redis-cli

# Testar conexão
ping
```

## 🧪 Testando a Instalação

### 1. Verificar Status dos Serviços
```bash
cd backend/docker
docker-compose ps
```

Todos os serviços devem estar com status "Up" e "healthy".

### 2. Testar Health Checks
```bash
# Auth Service
curl http://localhost:8001/health

# Agent Orchestrator
curl http://localhost:8002/health

# Document Service
curl http://localhost:8003/health

# Billing Service
curl http://localhost:8004/health
```

### 3. Testar Frontend
1. Acesse http://localhost:3000
2. Registre uma nova conta
3. Faça login
4. Teste o chat com o Agente Contábil
5. Faça upload de um documento

### 4. Verificar Logs
```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f auth-service
```

## 🔍 Solução de Problemas

### Problema: Docker não inicia
**Solução:**
- Windows: Reinicie o Docker Desktop
- Linux: `sudo systemctl start docker`
- Verifique se a virtualização está habilitada

### Problema: Porta já em uso
**Solução:**
```bash
# Verificar processos usando as portas
netstat -tulpn | grep :8001
netstat -tulpn | grep :3000

# Parar serviços conflitantes ou alterar portas no docker-compose.yml
```

### Problema: Erro de permissão no Docker
**Solução:**
```bash
# Linux: Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Windows: Executar como administrador
```

### Problema: Banco de dados não conecta
**Solução:**
```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps postgres-auth

# Verificar logs
docker-compose logs postgres-auth

# Recriar containers
docker-compose down
docker-compose up -d
```

### Problema: OpenAI API não funciona
**Solução:**
1. Verifique se a API key está correta no .env
2. Verifique se tem créditos na conta OpenAI
3. Teste a API key diretamente:
```bash
curl -H "Authorization: Bearer sk-your-key" https://api.openai.com/v1/models
```

### Problema: Frontend não carrega
**Solução:**
```bash
# Limpar cache do npm
npm cache clean --force

# Reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# Verificar se o backend está rodando
curl http://localhost:8001/health
```

## 📊 Monitoramento

### Verificar Uso de Recursos
```bash
# Uso de CPU e memória
docker stats

# Uso de disco
docker system df
```

### Limpeza de Recursos
```bash
# Parar todos os containers
docker-compose down

# Remover containers órfãos
docker-compose down --remove-orphans

# Limpar volumes não utilizados
docker volume prune

# Limpar imagens não utilizadas
docker image prune
```

## 🔄 Atualização

### Atualizar Código
```bash
git pull origin main
npm install
docker-compose down
docker-compose up -d --build
```

### Atualizar Dependências
```bash
# Frontend
npm update

# Backend (reconstruir containers)
docker-compose down
docker-compose up -d --build
```

## 📚 Comandos Úteis

### Desenvolvimento
```bash
# Iniciar ambiente completo
./scripts/start-dev.ps1  # Windows
./scripts/start-dev.sh   # Linux/Mac

# Parar serviços
docker-compose down

# Ver logs em tempo real
docker-compose logs -f

# Executar comandos em containers
docker-compose exec auth-service bash
docker-compose exec postgres-auth psql -U agenthub
```

### Produção
```bash
# Iniciar em modo produção
docker-compose -f docker-compose.prod.yml up -d

# Backup de banco de dados
docker-compose exec postgres-auth pg_dump -U agenthub auth_service > backup.sql

# Restaurar backup
docker-compose exec -T postgres-auth psql -U agenthub auth_service < backup.sql
```

## 🆘 Suporte

Se encontrar problemas:

1. **Verifique os logs**: `docker-compose logs -f`
2. **Consulte a documentação**: `docs/` directory
3. **Teste os health checks**: Verifique se todos os serviços estão saudáveis
4. **Reinicie os serviços**: `docker-compose restart`
5. **Recrie o ambiente**: `docker-compose down && docker-compose up -d`

Para mais ajuda, consulte o README.md principal ou abra uma issue no repositório.

