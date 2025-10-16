# 📚 Documentação AgentHub - Índice

Bem-vindo à documentação completa da plataforma AgentHub! Este índice organiza todos os documentos técnicos e guias do projeto.

## 🎯 **Documentos Principais**

### 📋 Visão Geral
- **[README Principal](../README.md)** - Visão geral do projeto e início rápido
- **[Resumo Executivo](PROJECT_SUMMARY.md)** - Resumo completo do que foi implementado
- **[Relatório de Status](STATUS_REPORT.md)** - O que foi feito vs. o que falta fazer

### 🚀 **Guias Práticos**
- **[Guia de Instalação](INSTALLATION.md)** - Instalação completa passo a passo
- **[Guia de Testes](TESTING.md)** - Checklist de testes e validação
- **[Diagramas de Arquitetura](architecture-diagram.md)** - Arquitetura detalhada da plataforma

## 🔧 **Documentação dos Serviços Backend**

### 📁 **Serviços Individuais**
- **[Auth Service](backend-services/auth-service.md)** - Autenticação e gerenciamento de usuários
- **[Agent Orchestrator](backend-services/agent-orchestrator.md)** - Orquestração de agentes e RAG
- **[Document Service](backend-services/document-service.md)** - Processamento de documentos e OCR
- **[Billing Service](backend-services/billing-service.md)** - Sistema de tokens e faturamento

## 📊 **Estrutura da Documentação**

```
docs/
├── README.md                           # Este índice
├── PROJECT_SUMMARY.md                  # Resumo executivo
├── STATUS_REPORT.md                    # Relatório de status
├── INSTALLATION.md                     # Guia de instalação
├── TESTING.md                          # Guia de testes
├── architecture-diagram.md             # Diagramas de arquitetura
└── backend-services/
    ├── auth-service.md                 # Documentação Auth Service
    ├── agent-orchestrator.md           # Documentação Agent Orchestrator
    ├── document-service.md             # Documentação Document Service
    └── billing-service.md              # Documentação Billing Service
```

## 🎯 **Para Diferentes Audiências**

### 👨‍💻 **Desenvolvedores**
Comece por:
1. [README Principal](../README.md) - Visão geral técnica
2. [Guia de Instalação](INSTALLATION.md) - Setup do ambiente
3. [Documentação dos Serviços](backend-services/) - Detalhes técnicos
4. [Guia de Testes](TESTING.md) - Validação e testes

### 🎓 **Acadêmicos/Avaliadores**
Comece por:
1. [Resumo Executivo](PROJECT_SUMMARY.md) - Visão geral do projeto
2. [Relatório de Status](STATUS_REPORT.md) - O que foi implementado
3. [Diagramas de Arquitetura](architecture-diagram.md) - Arquitetura técnica
4. [README Principal](../README.md) - Demonstração prática

### 🚀 **Para Deploy/Produção**
Comece por:
1. [Guia de Instalação](INSTALLATION.md) - Setup completo
2. [Guia de Testes](TESTING.md) - Validação antes do deploy
3. [Documentação dos Serviços](backend-services/) - Configurações específicas
4. [Relatório de Status](STATUS_REPORT.md) - Próximos passos

### 🔍 **Para Troubleshooting**
1. [Guia de Instalação](INSTALLATION.md) - Seção de solução de problemas
2. [Documentação dos Serviços](backend-services/) - Logs e monitoramento
3. [Guia de Testes](TESTING.md) - Comandos de debug
4. [README Principal](../README.md) - Comandos úteis

## 📖 **Navegação Rápida**

### 🏗️ **Arquitetura**
- [Diagrama Geral](architecture-diagram.md#diagrama-de-arquitetura-geral)
- [Fluxo de Dados](architecture-diagram.md#fluxo-de-dados---chat-com-agente)
- [Componentes de Segurança](architecture-diagram.md#componentes-de-segurança)

### 🔧 **Configuração**
- [Variáveis de Ambiente](INSTALLATION.md#configuração)
- [Docker Setup](INSTALLATION.md#configuração-do-docker)
- [Banco de Dados](INSTALLATION.md#configuração-do-banco-de-dados)

### 🧪 **Testes**
- [Checklist de Testes](TESTING.md#checklist-de-testes)
- [Testes de API](TESTING.md#testes-de-api)
- [Comandos de Debug](TESTING.md#comandos-de-debug)

### 🚀 **Deploy**
- [Scripts de Desenvolvimento](INSTALLATION.md#instalação-rápida)
- [Configuração de Produção](STATUS_REPORT.md#configuração-de-produção)
- [Monitoramento](STATUS_REPORT.md#configuração-de-produção)

## 🔍 **Busca Rápida por Tópico**

### Autenticação
- [Auth Service](backend-services/auth-service.md)
- [JWT Tokens](backend-services/auth-service.md#jwt-tokens)
- [Endpoints de Auth](backend-services/auth-service.md#endpoints-da-api)

### Agentes de IA
- [Agent Orchestrator](backend-services/agent-orchestrator.md)
- [Sistema RAG](backend-services/agent-orchestrator.md#sistema-rag)
- [Agente Contábil MEI](PROJECT_SUMMARY.md#agente-contábil-mei-100-concluído)

### Documentos
- [Document Service](backend-services/document-service.md)
- [OCR Processing](backend-services/document-service.md#processamento-ocr)
- [Upload de Arquivos](backend-services/document-service.md#upload-de-arquivos)

### Faturamento
- [Billing Service](backend-services/billing-service.md)
- [Sistema de Tokens](backend-services/billing-service.md#sistema-de-tokens)
- [Modelo de Negócio](backend-services/billing-service.md#modelo-de-negócio)

### Infraestrutura
- [Docker Setup](INSTALLATION.md#configuração-do-docker)
- [API Gateway](architecture-diagram.md#api-gateway)
- [Banco de Dados](INSTALLATION.md#configuração-do-banco-de-dados)

## 📞 **Suporte**

### 🆘 **Problemas Comuns**
1. Consulte a [seção de troubleshooting](INSTALLATION.md#solução-de-problemas)
2. Verifique os [logs dos serviços](TESTING.md#comandos-de-debug)
3. Execute os [health checks](TESTING.md#testes-de-api)

### 📝 **Contribuindo**
1. Leia o [README Principal](../README.md)
2. Siga o [Guia de Instalação](INSTALLATION.md)
3. Execute os [testes](TESTING.md) antes de contribuir

### 🔄 **Atualizações**
- A documentação é atualizada conforme o projeto evolui
- Versões são marcadas com data de atualização
- Mudanças significativas são documentadas no changelog

---

## 🎉 **Começar Agora**

**Novo no projeto?** Comece aqui:
1. **[README Principal](../README.md)** - Visão geral
2. **[Guia de Instalação](INSTALLATION.md)** - Setup
3. **[Guia de Testes](TESTING.md)** - Validação

**Precisa de ajuda específica?** Use o índice acima para encontrar o documento certo.

**Bem-vindo ao AgentHub!** 🚀
