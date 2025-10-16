# AgentHub Development Startup Script
# Este script inicia o ambiente de desenvolvimento completo

Write-Host "🚀 Iniciando AgentHub - Plataforma Inteligente de Automação" -ForegroundColor Green
Write-Host "==============================================================" -ForegroundColor Green

# Verificar se Docker está rodando
try {
    docker info | Out-Null
    Write-Host "✅ Docker está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker não está rodando. Por favor, inicie o Docker primeiro." -ForegroundColor Red
    exit 1
}

# Verificar se Docker Compose está disponível
if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker Compose não encontrado. Por favor, instale o Docker Compose." -ForegroundColor Red
    exit 1
}

# Navegar para o diretório do backend
Set-Location backend\docker

Write-Host "📦 Iniciando microsserviços..." -ForegroundColor Yellow
docker-compose up -d

Write-Host "⏳ Aguardando serviços ficarem prontos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar status dos serviços
Write-Host "🔍 Verificando status dos serviços..." -ForegroundColor Yellow
docker-compose ps

Write-Host ""
Write-Host "🌐 Serviços disponíveis:" -ForegroundColor Cyan
Write-Host "  - Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  - API Gateway: http://localhost:80" -ForegroundColor White
Write-Host "  - Auth Service: http://localhost:8001" -ForegroundColor White
Write-Host "  - Agent Orchestrator: http://localhost:8002" -ForegroundColor White
Write-Host "  - Document Service: http://localhost:8003" -ForegroundColor White
Write-Host "  - Billing Service: http://localhost:8004" -ForegroundColor White
Write-Host "  - MinIO Console: http://localhost:9001" -ForegroundColor White
Write-Host ""

# Verificar health dos serviços
Write-Host "🏥 Verificando saúde dos serviços..." -ForegroundColor Yellow

$services = @(
    @{Name="auth-service"; Port=8001},
    @{Name="agent-orchestrator"; Port=8002},
    @{Name="document-service"; Port=8003},
    @{Name="billing-service"; Port=8004}
)

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($service.Port)/health" -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "  ✅ $($service.Name) está saudável" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $($service.Name) não está respondendo" -ForegroundColor Red
        }
    } catch {
        Write-Host "  ❌ $($service.Name) não está respondendo" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Ambiente de desenvolvimento iniciado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Próximos passos:" -ForegroundColor Cyan
Write-Host "  1. Execute 'npm install' na raiz do projeto" -ForegroundColor White
Write-Host "  2. Execute 'npm run dev' para iniciar o frontend" -ForegroundColor White
Write-Host "  3. Acesse http://localhost:3000 para usar a plataforma" -ForegroundColor White
Write-Host ""
Write-Host "📚 Para parar os serviços: docker-compose down" -ForegroundColor Yellow
Write-Host "📋 Para ver logs: docker-compose logs -f" -ForegroundColor Yellow

# Voltar para o diretório raiz
Set-Location ..\..

