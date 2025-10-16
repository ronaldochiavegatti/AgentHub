# AgentHub - Plataforma Inteligente de Automação

Uma Arquitetura Escalável para Agentes de IA Verticalizados

## 📋 Visão Geral

O AgentHub é uma plataforma SaaS baseada em microsserviços que serve como ecossistema para agentes de Inteligência Artificial especializados. Este projeto implementa um agente contábil focado em Microempreendedores Individuais (MEI) como prova de conceito.

## 🏗️ Arquitetura

### Frontend
- **Next.js 15** com React 19
- **Tailwind CSS** para estilização
- **shadcn/ui** para componentes
- Interface responsiva e moderna

### Backend (Microsserviços)
- **Auth Service** (Porta 8001): Autenticação JWT e gerenciamento de usuários
- **Agent Orchestrator** (Porta 8002): Orquestração de agentes e RAG
- **Document Service** (Porta 8003): Processamento OCR e armazenamento
- **Billing Service** (Porta 8004): Gerenciamento de tokens e faturamento

### Infraestrutura
- **PostgreSQL**: Bancos de dados relacionais
- **MinIO**: Armazenamento de objetos (S3-compatível)
- **Redis**: Cache e filas
- **NGINX**: API Gateway
- **Docker**: Containerização

## 🚀 Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Node.js 18+ (para desenvolvimento frontend)
- Python 3.11+ (para desenvolvimento backend)

### 1. Executar Backend (Microsserviços)

```bash
# Navegar para o diretório do backend
cd backend/docker

# Executar todos os serviços
docker-compose up -d

# Verificar status dos serviços
docker-compose ps
```

### 2. Executar Frontend

```bash
# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev

# Acessar em http://localhost:3000
```

### 3. Acessar Serviços

- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:80
- **MinIO Console**: http://localhost:9001
- **Documentação API**: http://localhost:8001/docs (Auth Service)

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Frontend
NEXT_PUBLIC_API_URL=http://localhost

# Backend Services
DATABASE_URL=postgresql://agenthub:agenthub_password@localhost:5432/auth_service
GEMINI_API_KEY=your-gemini-api-key
SECRET_KEY=your-secret-key-change-in-production

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
```

### Configuração do Banco de Dados

Os bancos de dados são criados automaticamente via Docker. Para configurar manualmente:

```bash
# Executar scripts de criação
psql -h localhost -U agenthub -d auth_service -f backend/shared/database_schemas.sql
```

## 📱 Funcionalidades

### 1. Autenticação
- Registro e login de usuários
- JWT para autenticação stateless
- Gerenciamento de sessões

### 2. Agente Contábil
- **Chat Inteligente**: Responde dúvidas sobre MEI usando RAG
- **Processamento de Documentos**: OCR + extração de dados estruturados
- **Base de Conhecimento**: Legislação fiscal atualizada

### 3. Sistema de Faturamento
- Modelo baseado em tokens
- Controle de saldo em tempo real
- Histórico de transações

### 4. Gerenciamento de Documentos
- Upload de notas fiscais (PDF, JPG, PNG)
- Processamento OCR automático
- Extração de dados estruturados

## 🔌 APIs

### Autenticação
```
POST /auth/register - Registrar usuário
POST /auth/login - Fazer login
GET /auth/me - Dados do usuário atual
POST /auth/verify-token - Verificar token
```

### Agentes
```
GET /agents - Listar agentes disponíveis
GET /agents/{id} - Detalhes do agente
POST /chat - Conversar com agente
POST /process-document - Processar documento
```

### Documentos
```
POST /documents/upload - Upload de documento
GET /documents/jobs/{id} - Status do processamento
GET /documents/jobs - Listar documentos do usuário
```

### Faturamento
```
GET /billing/balance/{user_id} - Saldo de tokens
POST /billing/charge-tokens - Cobrar tokens
GET /billing/transactions/{user_id} - Histórico
```

## 🧪 Testando a Plataforma

### 1. Registro e Login
1. Acesse http://localhost:3000
2. Registre uma nova conta ou use as credenciais demo
3. Faça login e acesse o dashboard

### 2. Chat com Agente Contábil
1. Vá para "Falar com Agente Contábil"
2. Faça perguntas sobre MEI, como:
   - "Quais são os novos prazos para a declaração do MEI?"
   - "Como calcular o DAS mensal?"
   - "Quais documentos preciso guardar?"

### 3. Upload de Documentos
1. Acesse "Gerenciamento de Documentos"
2. Faça upload de uma nota fiscal (PDF ou imagem)
3. Acompanhe o processamento em tempo real

### 4. Verificar Faturamento
1. Acesse "Faturamento" no menu
2. Visualize saldo de tokens e histórico de uso

## 📊 Monitoramento

### Health Checks
Todos os serviços expõem endpoints de health check:
- Auth Service: http://localhost:8001/health
- Agent Orchestrator: http://localhost:8002/health
- Document Service: http://localhost:8003/health
- Billing Service: http://localhost:8004/health

### Logs
```bash
# Ver logs de todos os serviços
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f auth-service
```

## 🔒 Segurança

- Autenticação JWT com tokens seguros
- Validação de entrada em todas as APIs
- Rate limiting no API Gateway
- Isolamento de serviços via Docker
- CORS configurado adequadamente

## 🚧 Desenvolvimento

### Estrutura do Projeto
```
AgentHub/
├── app/                    # Frontend Next.js
├── components/            # Componentes React
├── backend/
│   ├── services/         # Microsserviços
│   ├── shared/           # Modelos compartilhados
│   └── docker/           # Configuração Docker
└── docs/                 # Documentação
```

### Adicionando Novos Agentes

1. **Criar configuração no banco**:
```sql
INSERT INTO agents (name, description, category) VALUES 
('Novo Agente', 'Descrição', 'categoria');

INSERT INTO agent_capabilities (agent_id, capability_type, config_json) VALUES 
(agent_id, 'chat', '{"system_prompt": "..."}');
```

2. **Adicionar conhecimento**:
```sql
INSERT INTO knowledge_base (agent_id, title, content, content_type) VALUES 
(agent_id, 'Título', 'Conteúdo', 'documentation');
```

## 📈 Próximos Passos

- [ ] Implementar agentes adicionais (Jurídico, Financeiro)
- [ ] Painel administrativo
- [ ] Personalização de agentes por usuário
- [ ] Integração com APIs externas
- [ ] Métricas e analytics avançados
- [ ] Deploy em produção

## 📄 Licença

Este projeto foi desenvolvido como Trabalho de Graduação para o curso de Análise e Desenvolvimento de Sistemas da FATEC.

## 👥 Contribuição

Para contribuir com o projeto:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Desenvolvido com ❤️ para demonstrar a viabilidade de plataformas de IA escaláveis e modulares.**

