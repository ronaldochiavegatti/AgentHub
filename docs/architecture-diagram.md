# AgentHub - Arquitetura da Plataforma

## Diagrama de Arquitetura Geral

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                    FRONTEND                                     │
│                          Next.js + React + Tailwind CSS                        │
│                              (Porta 3000)                                     │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  │ HTTP/HTTPS
                  │
┌─────────────────▼───────────────────────────────────────────────────────────────┐
│                               API GATEWAY                                       │
│                                NGINX                                           │
│                              (Porta 80/443)                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ /auth/*         │  │ /agents/*       │  │ /documents/*    │  │ /billing/*   │ │
│  │ → Auth Service  │  │ → Orchestrator  │  │ → Document Svc  │  │ → Billing Svc│ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  │ Internal Network (Docker)
                  │
┌─────────────────▼───────────────────────────────────────────────────────────────┐
│                               MICROSERVIÇOS                                    │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ Auth Service    │  │ Agent           │  │ Document        │  │ Billing      │ │
│  │ (Porta 8001)    │  │ Orchestrator    │  │ Service         │  │ Service      │ │
│  │                 │  │ (Porta 8002)    │  │ (Porta 8003)    │  │ (Porta 8004) │ │
│  │ • JWT Auth      │  │ • RAG Engine    │  │ • OCR Process   │  │ • Token Mgmt │ │
│  │ • User Mgmt     │  │ • Chat Logic    │  │ • File Storage  │  │ • Pricing    │ │
│  │ • Sessions      │  │ • Agent Config  │  │ • Data Extract  │  │ • Billing    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  │ Database Connections
                  │
┌─────────────────▼───────────────────────────────────────────────────────────────┐
│                               BANCO DE DADOS                                   │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │ PostgreSQL      │  │ PostgreSQL      │  │ PostgreSQL      │  │ PostgreSQL   │ │
│  │ Auth Service    │  │ Agent           │  │ Document        │  │ Billing      │ │
│  │ (Porta 5432)    │  │ Orchestrator    │  │ Service         │  │ Service      │ │
│  │                 │  │ (Porta 5433)    │  │ (Porta 5434)    │  │ (Porta 5435) │ │
│  │ • users         │  │ • agents        │  │ • document_jobs │  │ • user_tokens│ │
│  │ • sessions      │  │ • capabilities  │  │ • results       │  │ • transactions│ │
│  │                 │  │ • conversations │  │                 │  │ • pricing    │ │
│  │                 │  │ • knowledge_base│  │                 │  │              │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────┬───────────────────────────────────────────────────────────────┘
                  │
                  │ Cache & Storage
                  │
┌─────────────────▼───────────────────────────────────────────────────────────────┐
│                           INFRAESTRUTURA AUXILIAR                              │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Redis           │  │ MinIO           │  │ OpenAI API      │                │
│  │ (Porta 6379)    │  │ (Porta 9000)    │  │ (External)      │                │
│  │                 │  │                 │  │                 │                │
│  │ • Cache         │  │ • File Storage  │  │ • LLM           │                │
│  │ • Sessions      │  │ • Documents     │  │ • Embeddings    │                │
│  │ • Queues        │  │ • Images        │  │ • RAG           │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados - Chat com Agente

```
1. Usuário → Frontend
   ├── Digita pergunta no chat
   └── Envia requisição para API Gateway

2. API Gateway → Agent Orchestrator
   ├── Roteia para /agents/chat
   └── Valida token JWT

3. Agent Orchestrator
   ├── Verifica token com Auth Service
   ├── Busca agente e configurações
   ├── Pesquisa base de conhecimento (RAG)
   ├── Gera resposta via OpenAI API
   ├── Cobra tokens via Billing Service
   └── Retorna resposta

4. Frontend ← API Gateway ← Agent Orchestrator
   └── Exibe resposta no chat
```

## Fluxo de Dados - Upload de Documento

```
1. Usuário → Frontend
   ├── Seleciona arquivo (PDF/Imagem)
   └── Envia para Document Service

2. Document Service
   ├── Valida token com Auth Service
   ├── Armazena arquivo no MinIO
   ├── Cria job de processamento
   ├── Inicia processamento OCR (background)
   └── Retorna job_id

3. Processamento Background
   ├── Download arquivo do MinIO
   ├── Executa OCR (Tesseract)
   ├── Extrai dados via LLM
   ├── Atualiza status do job
   └── Armazena resultados

4. Frontend
   ├── Polling do status do job
   └── Exibe resultados quando concluído
```

## Componentes de Segurança

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SEGURANÇA                                         │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ JWT Tokens      │  │ Rate Limiting   │  │ Input Validation│                │
│  │                 │  │                 │  │                 │                │
│  │ • Stateless     │  │ • NGINX         │  │ • Pydantic      │                │
│  │ • Expiration    │  │ • Per Service   │  │ • SQL Injection │                │
│  │ • Refresh       │  │ • Per User      │  │ • XSS Protection│                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ CORS            │  │ HTTPS           │  │ Container       │                │
│  │                 │  │                 │  │ Security        │                │
│  │ • Configured    │  │ • TLS/SSL       │  │ • Non-root      │                │
│  │ • Origins       │  │ • Certificates  │  │ • Read-only     │                │
│  │ • Methods       │  │ • HSTS          │  │ • Minimal       │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Escalabilidade

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            ESCALABILIDADE                                      │
│                                                                                 │
│  Horizontal Scaling:                                                           │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Load Balancer   │  │ Multiple        │  │ Database        │                │
│  │                 │  │ Instances       │  │ Clustering      │                │
│  │ • NGINX         │  │ • Docker        │  │ • Read Replicas │                │
│  │ • HAProxy       │  │ • Kubernetes    │  │ • Sharding      │                │
│  │ • AWS ALB       │  │ • Auto-scaling  │  │ • Connection    │                │
│  └─────────────────┘  └─────────────────┘  │ Pooling         │                │
│                                            └─────────────────┘                │
│                                                                                 │
│  Vertical Scaling:                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ CPU             │  │ Memory          │  │ Storage         │                │
│  │                 │  │                 │  │                 │                │
│  │ • More cores    │  │ • RAM increase  │  │ • SSD/NVMe      │                │
│  │ • Faster CPU    │  │ • Cache size    │  │ • RAID config   │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Monitoramento e Observabilidade

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          MONITORAMENTO                                         │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Health Checks   │  │ Logging         │  │ Metrics         │                │
│  │                 │  │                 │  │                 │                │
│  │ • /health       │  │ • Structured    │  │ • Prometheus    │                │
│  │ • Database      │  │ • JSON format   │  │ • Grafana       │                │
│  │ • Dependencies  │  │ • Centralized   │  │ • Custom        │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
│                                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐                │
│  │ Error Tracking  │  │ Performance     │  │ Alerting        │                │
│  │                 │  │ Monitoring      │  │                 │                │
│  │ • Sentry        │  │ • APM           │  │ • Slack/Email   │                │
│  │ • Stack traces  │  │ • Response time │  │ • PagerDuty     │                │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Tecnologias e Versões

| Componente | Tecnologia | Versão | Propósito |
|------------|------------|--------|-----------|
| Frontend | Next.js | 15.2.4 | Interface do usuário |
| Frontend | React | 19 | Biblioteca de componentes |
| Frontend | Tailwind CSS | 4.1.9 | Estilização |
| API Gateway | NGINX | Alpine | Roteamento e proxy |
| Auth Service | FastAPI | 0.104.1 | Autenticação JWT |
| Agent Orchestrator | FastAPI | 0.104.1 | Orquestração de agentes |
| Document Service | FastAPI | 0.104.1 | Processamento de documentos |
| Billing Service | FastAPI | 0.104.1 | Gerenciamento de tokens |
| Database | PostgreSQL | 15 | Armazenamento relacional |
| Cache | Redis | 7-alpine | Cache e sessões |
| Storage | MinIO | Latest | Armazenamento de objetos |
| Container | Docker | Latest | Containerização |
| LLM | OpenAI API | 1.3.0 | Processamento de linguagem natural |
| OCR | Tesseract | 5.0 | Reconhecimento óptico de caracteres |

