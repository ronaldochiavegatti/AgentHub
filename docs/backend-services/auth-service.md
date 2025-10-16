# Auth Service - Documentação Técnica

## 📋 Visão Geral

O Auth Service é responsável por toda a autenticação e autorização da plataforma AgentHub. Gerencia usuários, sessões JWT e fornece endpoints seguros para autenticação.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    AUTH SERVICE                             │
│                      (Porta 8001)                          │
├─────────────────────────────────────────────────────────────┤
│  • JWT Authentication                                      │
│  • User Management                                         │
│  • Session Management                                      │
│  • Password Security                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                           │
│              (auth_service)                                │
├─────────────────────────────────────────────────────────────┤
│  • users table                                            │
│  • user_sessions table                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🗄️ Banco de Dados

### Tabela: users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: user_sessions
```sql
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT false
);
```

## 🔐 Segurança

### Hash de Senhas
- **Algoritmo**: SHA-256 com salt
- **Salt**: 16 bytes aleatórios por senha
- **Formato**: `salt:hash` armazenado no banco

### JWT Tokens
- **Algoritmo**: HS256
- **Expiração**: 30 minutos
- **Claims**: `sub` (user_id), `exp` (expiration)
- **Secret**: Configurável via variável de ambiente

## 📡 Endpoints da API

### POST /register
**Descrição**: Registra um novo usuário na plataforma

**Request Body**:
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123",
  "first_name": "João",
  "last_name": "Silva"
}
```

**Response**:
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "id": "uuid",
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Status Codes**:
- `200`: Registro bem-sucedido
- `400`: Email já existe ou dados inválidos
- `422`: Erro de validação

### POST /login
**Descrição**: Autentica usuário e retorna JWT token

**Request Body**:
```json
{
  "email": "usuario@exemplo.com",
  "password": "senha123"
}
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": {
    "id": "uuid",
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "is_active": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  }
}
```

**Status Codes**:
- `200`: Login bem-sucedido
- `401`: Credenciais inválidas
- `400`: Usuário inativo

### GET /me
**Descrição**: Retorna dados do usuário autenticado

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "id": "uuid",
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "last_name": "Silva",
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Codes**:
- `200`: Dados retornados
- `401`: Token inválido ou expirado

### POST /verify-token
**Descrição**: Verifica se um token JWT é válido

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "success": true,
  "message": "Token is valid",
  "data": {
    "user_id": "uuid"
  }
}
```

**Status Codes**:
- `200`: Token válido
- `401`: Token inválido ou expirado

### GET /health
**Descrição**: Health check do serviço

**Response**:
```json
{
  "status": "healthy",
  "service": "auth-service"
}
```

## 🔧 Configuração

### Variáveis de Ambiente
```env
DATABASE_URL=postgresql://agenthub:agenthub_password@localhost:5432/auth_service
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Dependências Python
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pydantic==2.5.0
python-dotenv==1.0.0
```

## 🚀 Execução

### Desenvolvimento
```bash
cd backend/services/auth-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### Docker
```bash
cd backend/docker
docker-compose up auth-service
```

### Health Check
```bash
curl http://localhost:8001/health
```

## 🔍 Monitoramento

### Logs
- **Estrutura**: JSON formatado
- **Níveis**: INFO, WARNING, ERROR
- **Localização**: stdout (Docker logs)

### Métricas
- **Requests/segundo**: Monitorar carga
- **Tempo de resposta**: < 100ms para auth
- **Taxa de erro**: < 1%
- **Tokens expirados**: Monitorar revogações

## 🧪 Testes

### Testes Unitários
```bash
# Criar testes para:
# - Hash de senhas
# - Geração de JWT
# - Validação de tokens
# - CRUD de usuários
```

### Testes de Integração
```bash
# Testar endpoints completos:
curl -X POST http://localhost:8001/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456","first_name":"Test","last_name":"User"}'

curl -X POST http://localhost:8001/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"123456"}'
```

## 🔒 Considerações de Segurança

### Produção
- [ ] Usar HTTPS em produção
- [ ] Rotacionar SECRET_KEY regularmente
- [ ] Implementar rate limiting
- [ ] Logs de auditoria para login/logout
- [ ] Implementar refresh tokens
- [ ] Validação de força de senha

### Backup
- [ ] Backup regular do banco auth_service
- [ ] Teste de restauração
- [ ] Documentação de procedimentos

## 📊 Performance

### Benchmarks Esperados
- **Login**: < 200ms
- **Registro**: < 300ms
- **Verificação de token**: < 50ms
- **Throughput**: 1000+ req/s

### Otimizações
- [ ] Índices no banco de dados
- [ ] Cache de sessões ativas
- [ ] Connection pooling
- [ ] Compressão de responses

## 🔄 Integração com Outros Serviços

### Agent Orchestrator
- Fornece verificação de tokens via `/verify-token`
- Usado para autenticar requisições de chat

### Billing Service
- Fornece user_id para transações
- Usado para associar uso de tokens a usuários

### Document Service
- Fornece autenticação para uploads
- Usado para associar documentos a usuários

