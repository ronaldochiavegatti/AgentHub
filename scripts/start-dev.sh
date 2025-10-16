#!/bin/bash

# AgentHub Development Startup Script
# Este script inicia o ambiente de desenvolvimento completo

echo "🚀 Iniciando AgentHub - Plataforma Inteligente de Automação"
echo "=============================================================="

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Por favor, inicie o Docker primeiro."
    exit 1
fi

# Verificar se Docker Compose está disponível
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não encontrado. Por favor, instale o Docker Compose."
    exit 1
fi

echo "✅ Docker está rodando"

# Navegar para o diretório do backend
cd backend/docker

echo "📦 Iniciando microsserviços..."
docker-compose up -d

echo "⏳ Aguardando serviços ficarem prontos..."
sleep 10

# Verificar status dos serviços
echo "🔍 Verificando status dos serviços..."
docker-compose ps

echo ""
echo "🌐 Serviços disponíveis:"
echo "  - Frontend: http://localhost:3000"
echo "  - API Gateway: http://localhost:80"
echo "  - Auth Service: http://localhost:8001"
echo "  - Agent Orchestrator: http://localhost:8002"
echo "  - Document Service: http://localhost:8003"
echo "  - Billing Service: http://localhost:8004"
echo "  - MinIO Console: http://localhost:9001"
echo ""

# Verificar health dos serviços
echo "🏥 Verificando saúde dos serviços..."

services=(
    "auth-service:8001"
    "agent-orchestrator:8002"
    "document-service:8003"
    "billing-service:8004"
)

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -f -s "http://localhost:$port/health" > /dev/null; then
        echo "  ✅ $name está saudável"
    else
        echo "  ❌ $name não está respondendo"
    fi
done

echo ""
echo "🎉 Ambiente de desenvolvimento iniciado com sucesso!"
echo ""
echo "📝 Próximos passos:"
echo "  1. Execute 'npm install' na raiz do projeto"
echo "  2. Execute 'npm run dev' para iniciar o frontend"
echo "  3. Acesse http://localhost:3000 para usar a plataforma"
echo ""
echo "📚 Para parar os serviços: docker-compose down"
echo "📋 Para ver logs: docker-compose logs -f"

