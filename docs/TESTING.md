# Guia de Testes - AgentHub

## 🧪 Testes da Plataforma Completa

Este documento descreve como testar todas as funcionalidades da plataforma AgentHub para garantir que está funcionando corretamente.

## 📋 Checklist de Testes

### ✅ Pré-requisitos
- [ ] Docker está rodando
- [ ] Todos os serviços estão "Up" e "healthy"
- [ ] Frontend está acessível em http://localhost:3000
- [ ] OpenAI API key está configurada

### 🔐 Testes de Autenticação

#### 1. Registro de Usuário
1. Acesse http://localhost:3000
2. Clique em "Cadastre-se"
3. Preencha os dados:
   - Nome: João Silva
   - Email: joao@teste.com
   - Senha: senha123
4. Clique em "Cadastrar"
5. **Resultado esperado**: Redirecionamento para o dashboard

#### 2. Login de Usuário
1. Acesse http://localhost:3000
2. Use as credenciais:
   - Email: demo@agenthub.com
   - Senha: qualquer senha
3. Clique em "Entrar"
4. **Resultado esperado**: Login bem-sucedido e acesso ao dashboard

#### 3. Login Demo
1. Acesse http://localhost:3000
2. Clique em "Entrar com Conta Demo"
3. **Resultado esperado**: Login automático com conta demo

### 🏠 Testes do Dashboard

#### 1. Visualização do Dashboard
1. Após login, verifique se o dashboard carrega
2. **Resultado esperado**: 
   - Saudação personalizada
   - Cards de ação (Enviar Documento, Falar com Agente)
   - Seção "Atividade Recente"
   - Seção "Seus Agentes Ativos"

#### 2. Navegação
1. Teste todos os links do menu:
   - Dashboard
   - Documentos
   - Agente Contábil
2. **Resultado esperado**: Navegação fluida entre páginas

#### 3. Header e Token Balance
1. Verifique se o header mostra:
   - Logo AgentHub
   - Menu de navegação
   - Saldo de tokens (1,250 tokens)
   - Menu do usuário
2. **Resultado esperado**: Interface completa e funcional

### 🤖 Testes do Agente Contábil

#### 1. Acesso ao Agente
1. Clique em "Falar com Agente Contábil" ou navegue para `/agent/accounting`
2. **Resultado esperado**: 
   - Página do agente carrega
   - Interface de chat visível
   - Perguntas sugeridas aparecem

#### 2. Perguntas Sugeridas
1. Clique em uma das perguntas sugeridas:
   - "Quais são os novos prazos para a declaração do MEI?"
   - "Como calcular o DAS mensal do MEI?"
   - "Quais documentos preciso guardar para a declaração anual?"
   - "Como emitir nota fiscal como MEI?"
2. **Resultado esperado**: Pergunta é inserida no campo de input

#### 3. Chat com o Agente
1. Digite uma pergunta no campo de chat
2. Pressione Enter ou clique no botão de enviar
3. **Resultado esperado**: 
   - Mensagem do usuário aparece
   - Resposta do agente é gerada
   - Saldo de tokens é atualizado

#### 4. Perguntas de Teste
Teste as seguintes perguntas:

**Pergunta 1**: "Quais são os novos prazos para a declaração do MEI?"
- **Resposta esperada**: Informações sobre DASN-SIMEI e prazo de 31 de maio

**Pergunta 2**: "Como calcular o DAS mensal?"
- **Resposta esperada**: Valores específicos para cada atividade (R$ 65,00 para comércio/serviços)

**Pergunta 3**: "Posso contratar funcionários como MEI?"
- **Resposta esperada**: Sim, até 1 funcionário com informações sobre encargos

**Pergunta 4**: "Qual o limite de faturamento do MEI?"
- **Resposta esperada**: R$ 81.000,00 por ano (R$ 6.750,00 por mês)

### 📄 Testes de Upload de Documentos

#### 1. Acesso à Página de Documentos
1. Navegue para "Gerenciamento de Documentos" ou `/documents`
2. **Resultado esperado**: 
   - Página carrega com interface de upload
   - Lista de documentos existentes
   - Área de drag-and-drop

#### 2. Upload por Drag-and-Drop
1. Arraste um arquivo PDF ou imagem para a área de upload
2. **Resultado esperado**: 
   - Área fica destacada
   - Arquivo é processado

#### 3. Upload por Seleção
1. Clique em "Selecionar Arquivos"
2. Escolha um arquivo (PDF, JPG, PNG)
3. **Resultado esperado**: 
   - Upload iniciado
   - Status "Processando..." aparece

#### 4. Verificação de Status
1. Aguarde o processamento (pode levar alguns segundos)
2. Verifique se o status muda para "Concluído"
3. **Resultado esperado**: 
   - Status atualizado
   - Dados extraídos disponíveis

#### 5. Visualização de Resultados
1. Clique em "Ver Detalhes" em um documento processado
2. **Resultado esperado**: 
   - Página de detalhes carrega
   - Dados extraídos são exibidos
   - Opção de download

### 💰 Testes de Faturamento

#### 1. Acesso ao Faturamento
1. Clique no saldo de tokens no header ou navegue para `/billing`
2. **Resultado esperado**: 
   - Página de faturamento carrega
   - Saldo atual é exibido
   - Histórico de transações

#### 2. Verificação de Saldo
1. Verifique se o saldo inicial é 1,250 tokens
2. **Resultado esperado**: Saldo correto exibido

#### 3. Uso de Tokens
1. Use o chat do agente contábil
2. Verifique se o saldo diminui após cada interação
3. **Resultado esperado**: 
   - Saldo atualizado em tempo real
   - Transação registrada no histórico

#### 4. Histórico de Transações
1. Verifique o histórico de transações
2. **Resultado esperado**: 
   - Lista de transações
   - Detalhes de cada uso
   - Timestamps corretos

### 🔧 Testes de API

#### 1. Health Checks
Teste os endpoints de health check:

```bash
# Auth Service
curl http://localhost:8001/health

# Agent Orchestrator
curl http://localhost:8002/health

# Document Service
curl http://localhost:8003/health

# Billing Service
curl http://localhost:8004/health

# API Gateway
curl http://localhost/health
```

**Resultado esperado**: Todos retornam `{"status": "healthy"}`

#### 2. Autenticação via API
```bash
# Login
curl -X POST http://localhost/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@agenthub.com", "password": "senha123"}'

# Resultado esperado: Token JWT retornado
```

#### 3. Listar Agentes
```bash
# Listar agentes disponíveis
curl http://localhost/agents/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Resultado esperado: Lista de agentes com Agente Contábil
```

### 🐛 Testes de Erro

#### 1. Login com Credenciais Inválidas
1. Tente fazer login com email/senha incorretos
2. **Resultado esperado**: Mensagem de erro apropriada

#### 2. Upload de Arquivo Inválido
1. Tente fazer upload de um arquivo não suportado (ex: .txt)
2. **Resultado esperado**: Mensagem de erro sobre tipo de arquivo

#### 3. Upload de Arquivo Muito Grande
1. Tente fazer upload de um arquivo > 10MB
2. **Resultado esperado**: Mensagem de erro sobre tamanho do arquivo

#### 4. Chat sem Token
1. Use o chat até esgotar os tokens
2. **Resultado esperado**: Mensagem sobre saldo insuficiente

### 📊 Testes de Performance

#### 1. Tempo de Resposta
1. Meça o tempo de resposta do chat (deve ser < 5 segundos)
2. Meça o tempo de upload de documentos (deve ser < 10 segundos)
3. **Resultado esperado**: Respostas rápidas e responsivas

#### 2. Múltiplas Requisições
1. Faça várias perguntas no chat rapidamente
2. **Resultado esperado**: Sistema mantém estabilidade

#### 3. Upload Simultâneo
1. Faça upload de vários documentos ao mesmo tempo
2. **Resultado esperado**: Todos são processados corretamente

## 📝 Relatório de Testes

### Template de Relatório
```
Data do Teste: [DATA]
Versão Testada: 1.0.0
Ambiente: Desenvolvimento
Testador: [NOME]

RESULTADOS:
✅ Autenticação: PASSOU/FALHOU
✅ Dashboard: PASSOU/FALHOU  
✅ Chat do Agente: PASSOU/FALHOU
✅ Upload de Documentos: PASSOU/FALHOU
✅ Faturamento: PASSOU/FALHOU
✅ APIs: PASSOU/FALHOU

PROBLEMAS ENCONTRADOS:
- [Listar problemas encontrados]

OBSERVAÇÕES:
- [Observações adicionais]
```

### Critérios de Aprovação
- ✅ Todos os testes de funcionalidade passam
- ✅ Performance está dentro dos limites aceitáveis
- ✅ Interface está responsiva e intuitiva
- ✅ Dados são persistidos corretamente
- ✅ Sistema é estável sob carga normal

## 🔧 Comandos de Debug

### Ver Logs em Tempo Real
```bash
cd backend/docker
docker-compose logs -f
```

### Verificar Status dos Containers
```bash
docker-compose ps
```

### Reiniciar Serviços
```bash
docker-compose restart
```

### Limpar e Recriar
```bash
docker-compose down
docker-compose up -d --build
```

### Acessar Container para Debug
```bash
# Acessar banco de dados
docker-compose exec postgres-auth psql -U agenthub -d auth_service

# Acessar serviço
docker-compose exec auth-service bash
```

## 📚 Recursos Adicionais

- **Documentação da API**: http://localhost:8001/docs
- **MinIO Console**: http://localhost:9001
- **Logs Centralizados**: `docker-compose logs`
- **Monitoramento**: `docker stats`

Este guia garante que todas as funcionalidades principais da plataforma estão funcionando corretamente antes de considerar o sistema pronto para uso.

