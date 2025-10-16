# Billing Service - Documentação Técnica

## 📋 Visão Geral

O Billing Service é responsável pelo gerenciamento de tokens, faturamento e controle de uso na plataforma AgentHub. Implementa um modelo de negócio baseado em consumo de tokens, permitindo monetização flexível dos serviços de IA.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                   BILLING SERVICE                          │
│                     (Porta 8004)                          │
├─────────────────────────────────────────────────────────────┤
│  • Token Management                                       │
│  • Usage Tracking                                         │
│  • Pricing Configuration                                  │
│  • Transaction History                                    │
│  • Balance Control                                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                           │
│              (billing_service)                             │
├─────────────────────────────────────────────────────────────┤
│  • user_tokens table                                      │
│  • token_transactions table                               │
│  • pricing_config table                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              EXTERNAL INTEGRATIONS                         │
├─────────────────────────────────────────────────────────────┤
│  • Auth Service (user verification)                       │
│  • Agent Orchestrator (usage reporting)                   │
│  • Document Service (processing costs)                     │
└─────────────────────────────────────────────────────────────┘
```

## 🗄️ Banco de Dados

### Tabela: user_tokens
```sql
CREATE TABLE user_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    balance INTEGER DEFAULT 0,
    total_purchased INTEGER DEFAULT 0,
    total_used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: token_transactions
```sql
CREATE TABLE token_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount INTEGER NOT NULL,
    service_type VARCHAR(50),
    agent_id UUID,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: pricing_config
```sql
CREATE TABLE pricing_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_type VARCHAR(50) NOT NULL,
    token_cost INTEGER NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 💰 Modelo de Negócio

### Sistema de Tokens
- **Saldo Inicial**: 1,000 tokens gratuitos para novos usuários
- **Cobrança por Uso**: Baseada no tipo de serviço
- **Transparência**: Histórico completo de transações
- **Flexibilidade**: Configuração dinâmica de preços

### Preços por Serviço
```json
{
  "chat": 10,
  "document_processing": 50,
  "analysis": 25
}
```

### Tipos de Transação
- **USAGE**: Cobrança por uso de serviços (valor negativo)
- **PURCHASE**: Compra de tokens (valor positivo)
- **REFUND**: Reembolso de tokens (valor positivo)

## 📡 Endpoints da API

### GET /balance/{user_id}
**Descrição**: Obtém saldo de tokens do usuário

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "user_id": "uuid",
  "balance": 1250,
  "total_purchased": 2000,
  "total_used": 750
}
```

**Status Codes**:
- `200`: Saldo retornado
- `401`: Token inválido
- `403`: Acesso negado

### POST /charge-tokens
**Descrição**: Cobra tokens por uso de serviço

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**:
```json
{
  "user_id": "uuid",
  "service_type": "chat",
  "tokens_used": 15,
  "agent_id": "uuid",
  "description": "Chat interaction with accounting agent"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Tokens charged successfully",
  "data": {
    "new_balance": 1235,
    "tokens_used": 15
  }
}
```

**Validações**:
- Saldo suficiente
- Tipo de serviço válido
- Usuário autenticado

### POST /purchase-tokens
**Descrição**: Compra de tokens (implementação futura)

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Request Body**:
```json
{
  "user_id": "uuid",
  "amount": 1000,
  "payment_method": "credit_card"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Tokens purchased successfully",
  "data": {
    "new_balance": 2235,
    "tokens_purchased": 1000
  }
}
```

### GET /transactions/{user_id}
**Descrição**: Histórico de transações do usuário

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
- `limit`: Número máximo de resultados (padrão: 50)
- `type`: Filtrar por tipo de transação

**Response**:
```json
[
  {
    "id": "uuid",
    "user_id": "uuid",
    "transaction_type": "usage",
    "amount": -15,
    "service_type": "chat",
    "agent_id": "uuid",
    "description": "Chat interaction with accounting agent",
    "created_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": "uuid",
    "user_id": "uuid",
    "transaction_type": "purchase",
    "amount": 1000,
    "description": "Token purchase via credit_card",
    "created_at": "2024-01-15T09:15:00Z"
  }
]
```

### GET /pricing
**Descrição**: Configurações de preço atuais

**Response**:
```json
[
  {
    "id": "uuid",
    "service_type": "chat",
    "token_cost": 10,
    "description": "Custo por mensagem no chat com agente",
    "is_active": true,
    "created_at": "2024-01-15T08:00:00Z"
  },
  {
    "id": "uuid",
    "service_type": "document_processing",
    "token_cost": 50,
    "description": "Custo por processamento de documento via OCR",
    "is_active": true,
    "created_at": "2024-01-15T08:00:00Z"
  }
]
```

### POST /pricing
**Descrição**: Criar nova configuração de preço (admin)

**Headers**:
```
Authorization: Bearer <admin_jwt_token>
```

**Request Body**:
```json
{
  "service_type": "advanced_analysis",
  "token_cost": 100,
  "description": "Análise avançada de documentos",
  "is_active": true
}
```

## 🔧 Configuração

### Variáveis de Ambiente
```env
DATABASE_URL=postgresql://agenthub:agenthub_password@localhost:5435/billing_service
AUTH_SERVICE_URL=http://localhost:8001
DEFAULT_TOKEN_BALANCE=1000
TOKEN_PURCHASE_RATE=1.0
```

### Dependências Python
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
httpx==0.25.2
pydantic==2.5.0
python-dotenv==1.0.0
```

### Configurações Padrão
```python
DEFAULT_PRICING = [
    {"service_type": "chat", "token_cost": 10, "description": "Chat com agente"},
    {"service_type": "document_processing", "token_cost": 50, "description": "Processamento de documento"},
    {"service_type": "analysis", "token_cost": 25, "description": "Análise de documento"}
]
```

## 🚀 Execução

### Desenvolvimento
```bash
cd backend/services/billing-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8004 --reload
```

### Docker
```bash
cd backend/docker
docker-compose up billing-service
```

### Health Check
```bash
curl http://localhost:8004/health
```

## 🔍 Monitoramento

### Métricas Importantes
- **Token Usage Rate**: Tokens consumidos por hora
- **Revenue per User**: Receita média por usuário
- **Service Popularity**: Uso por tipo de serviço
- **Balance Distribution**: Distribuição de saldos
- **Transaction Volume**: Volume de transações

### Logs Estruturados
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "billing-service",
  "event": "tokens_charged",
  "user_id": "uuid",
  "service_type": "chat",
  "tokens_used": 15,
  "new_balance": 1235
}
```

## 🧪 Testes

### Testes de Cobrança
```python
async def test_charge_tokens():
    """Testa cobrança de tokens"""
    response = await charge_tokens(
        user_id="test-user",
        service_type="chat",
        tokens_used=10
    )
    assert response["success"] == True
    assert response["data"]["new_balance"] == 990
```

### Testes de Saldo Insuficiente
```python
async def test_insufficient_balance():
    """Testa cobrança com saldo insuficiente"""
    with pytest.raises(HTTPException) as exc_info:
        await charge_tokens(
            user_id="test-user",
            service_type="document_processing",
            tokens_used=10000
        )
    assert exc_info.value.status_code == 402
```

### Testes de Integração
```bash
# Verificar saldo
curl http://localhost:8004/billing/balance/$USER_ID \
  -H "Authorization: Bearer $JWT_TOKEN"

# Cobrar tokens
curl -X POST http://localhost:8004/billing/charge-tokens \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "'$USER_ID'",
    "service_type": "chat",
    "tokens_used": 10,
    "description": "Test charge"
  }'
```

## 🔒 Segurança

### Validações
- **Authentication**: JWT obrigatório
- **Authorization**: Usuários só acessam seus dados
- **Input Validation**: Validação rigorosa de entrada
- **Balance Checks**: Verificação de saldo antes de cobrança

### Considerações de Produção
- [ ] Rate limiting por usuário
- [ ] Logs de auditoria para transações
- [ ] Backup de dados financeiros
- [ ] Criptografia de dados sensíveis
- [ ] Integração com gateway de pagamento

## 📊 Relatórios e Analytics

### Dashboard de Métricas
```python
async def get_user_analytics(user_id: str):
    """Analytics do usuário"""
    return {
        "total_spent": 750,
        "most_used_service": "chat",
        "average_session_cost": 25,
        "usage_trend": "increasing"
    }
```

### Relatórios Administrativos
- **Revenue by Service**: Receita por tipo de serviço
- **User Retention**: Retenção de usuários
- **Usage Patterns**: Padrões de uso
- **Cost Analysis**: Análise de custos

## 🔄 Integração com Outros Serviços

### Auth Service
- Verifica tokens JWT
- Valida permissões de usuário
- Obtém dados do usuário

### Agent Orchestrator
- Recebe notificações de uso
- Cobra tokens por interações
- Registra uso por agente

### Document Service
- Cobra tokens por processamento
- Registra custos por documento
- Monitora uso de OCR

## 📈 Escalabilidade

### Horizontal Scaling
- **Stateless Design**: Sem estado local
- **Database Sharding**: Por usuário ou região
- **Load Balancing**: Múltiplas instâncias

### Vertical Scaling
- **CPU**: Para cálculos de billing
- **Memory**: Para cache de preços
- **Storage**: Para histórico de transações

## 💡 Funcionalidades Futuras

### 1. Sistema de Assinaturas
```python
class SubscriptionPlan:
    name: str
    monthly_tokens: int
    price: float
    features: List[str]
```

### 2. Promoções e Descontos
```python
class PromoCode:
    code: str
    discount_percentage: float
    valid_until: datetime
    usage_limit: int
```

### 3. Relatórios Detalhados
- **Exportação CSV/Excel**
- **Gráficos interativos**
- **Alertas de uso**
- **Previsão de gastos**

### 4. Integração de Pagamentos
- **Stripe/PayPal**
- **PIX brasileiro**
- **Cartão de crédito**
- **Boleto bancário**

## 🚨 Tratamento de Erros

### Erros Comuns
- **Insufficient Balance**: HTTP 402, saldo insuficiente
- **Invalid Service Type**: HTTP 400, tipo inválido
- **Unauthorized Access**: HTTP 403, acesso negado
- **Transaction Failed**: HTTP 500, erro interno

### Recovery Procedures
```python
async def recover_failed_transaction(transaction_id: str):
    """Recupera transação falhada"""
    # Implementar lógica de rollback
    # Registrar erro para análise
    # Notificar usuário se necessário
```

## 📋 Checklist de Produção

### Segurança
- [ ] HTTPS obrigatório
- [ ] Validação de entrada rigorosa
- [ ] Logs de auditoria
- [ ] Backup de dados financeiros

### Performance
- [ ] Cache de configurações de preço
- [ ] Otimização de queries
- [ ] Monitoramento de latência
- [ ] Alertas de performance

### Compliance
- [ ] LGPD compliance
- [ ] Auditoria de transações
- [ ] Retenção de dados
- [ ] Relatórios regulatórios


