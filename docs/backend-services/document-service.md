# Document Service - Documentação Técnica

## 📋 Visão Geral

O Document Service é responsável pelo processamento de documentos na plataforma AgentHub. Gerencia uploads, executa OCR (Optical Character Recognition), extrai dados estruturados usando LLMs e armazena arquivos de forma segura.

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                  DOCUMENT SERVICE                          │
│                     (Porta 8003)                          │
├─────────────────────────────────────────────────────────────┤
│  • File Upload & Validation                               │
│  • OCR Processing (Tesseract)                             │
│  • Data Extraction (LLM)                                  │
│  • File Storage (MinIO)                                   │
│  • Job Management                                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                           │
│             (document_service)                             │
├─────────────────────────────────────────────────────────────┤
│  • document_jobs table                                    │
│  • document_results table                                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              MINIO OBJECT STORAGE                          │
│                   (Porta 9000)                            │
├─────────────────────────────────────────────────────────────┤
│  • documents/ bucket                                      │
│  • User-specific folders                                  │
│  • File versioning                                        │
└─────────────────────────────────────────────────────────────┘
```

## 🗄️ Banco de Dados

### Tabela: document_jobs
```sql
CREATE TABLE document_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    ocr_result JSONB,
    extracted_data JSONB,
    error_message TEXT,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: document_results
```sql
CREATE TABLE document_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES document_jobs(id) ON DELETE CASCADE,
    result_type VARCHAR(50) NOT NULL,
    extracted_fields JSONB NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Funcionalidades Principais

### 1. Upload de Arquivos
- **Validação de tipo**: PDF, JPG, PNG, XLSX
- **Validação de tamanho**: Máximo 10MB
- **Armazenamento seguro**: MinIO com estrutura organizada
- **Metadados**: Informações detalhadas do arquivo

### 2. Processamento OCR
- **Engine**: Tesseract OCR com suporte a português
- **Formatos suportados**: PDF, imagens (JPG, PNG)
- **Precisão**: Configurável por tipo de documento
- **Background processing**: Processamento assíncrono

### 3. Extração de Dados
- **LLM Integration**: OpenAI GPT para extração inteligente
- **Estruturação**: Dados em formato JSON padronizado
- **Validação**: Verificação de campos obrigatórios
- **Confiança**: Score de confiança da extração

### 4. Gerenciamento de Jobs
- **Status tracking**: Pending → Processing → Completed/Failed
- **Retry logic**: Reprocessamento em caso de falha
- **Progress monitoring**: Timestamps de início e fim
- **Error handling**: Mensagens detalhadas de erro

## 📡 Endpoints da API

### POST /upload
**Descrição**: Upload de documento para processamento

**Headers**:
```
Authorization: Bearer <jwt_token>
Content-Type: multipart/form-data
```

**Request Body**:
```
file: [arquivo PDF/JPEG/PNG/XLSX]
```

**Response**:
```json
{
  "job_id": "uuid",
  "filename": "nota_fiscal_001.pdf",
  "status": "pending",
  "message": "Document uploaded successfully"
}
```

**Validações**:
- Tipo de arquivo permitido
- Tamanho máximo 10MB
- Usuário autenticado

### GET /jobs/{job_id}
**Descrição**: Obtém status e resultados de um job

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "filename": "nota_fiscal_001.pdf",
  "original_filename": "nota_fiscal_001.pdf",
  "file_path": "documents/user123/file.pdf",
  "file_size": 2048000,
  "mime_type": "application/pdf",
  "status": "completed",
  "ocr_result": {
    "text": "NOTA FISCAL DE SERVIÇOS...",
    "confidence": 0.95,
    "bounding_boxes": []
  },
  "extracted_data": {
    "cnpj_emitente": "12.345.678/0001-90",
    "valor_total": "1500.00",
    "data_emissao": "2024-01-15"
  },
  "processing_started_at": "2024-01-15T10:30:00Z",
  "processing_completed_at": "2024-01-15T10:32:15Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:32:15Z"
}
```

### GET /jobs
**Descrição**: Lista jobs do usuário autenticado

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Query Parameters**:
- `limit`: Número máximo de resultados (padrão: 50)
- `status`: Filtrar por status específico

**Response**:
```json
[
  {
    "id": "uuid",
    "filename": "nota_fiscal_001.pdf",
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### GET /download/{job_id}
**Descrição**: Download do arquivo original

**Headers**:
```
Authorization: Bearer <jwt_token>
```

**Response**:
- **Content-Type**: Baseado no mime_type original
- **Content-Disposition**: attachment; filename="original_filename"
- **Body**: Conteúdo binário do arquivo

## 🔄 Fluxo de Processamento

### 1. Upload
```
Usuário → Frontend → Document Service → MinIO
                                    ↓
                              Job criado (status: pending)
```

### 2. Processamento Assíncrono
```
Background Task:
1. Download do MinIO
2. OCR Processing (Tesseract)
3. LLM Data Extraction
4. Update job status
5. Store results
```

### 3. Resultados
```
Frontend polling → Job status → Results available
```

## 🔧 Configuração

### Variáveis de Ambiente
```env
DATABASE_URL=postgresql://agenthub:agenthub_password@localhost:5434/document_service
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=documents
MINIO_SECURE=false
AUTH_SERVICE_URL=http://localhost:8001
AGENT_ORCHESTRATOR_URL=http://localhost:8002
TESSERACT_CMD=tesseract
TESSERACT_LANG=por
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
minio==7.2.0
pillow==10.1.0
pytesseract==0.3.10
```

### Configuração do Tesseract
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr tesseract-ocr-por

# macOS
brew install tesseract tesseract-lang

# Windows
# Baixar do GitHub: https://github.com/UB-Mannheim/tesseract/wiki
```

## 🚀 Execução

### Desenvolvimento
```bash
cd backend/services/document-service
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

### Docker
```bash
cd backend/docker
docker-compose up document-service
```

### Health Check
```bash
curl http://localhost:8003/health
```

## 🔍 Monitoramento

### Métricas Importantes
- **Upload Success Rate**: > 99%
- **OCR Accuracy**: > 90%
- **Processing Time**: < 30 segundos por documento
- **Storage Usage**: Monitorar crescimento do MinIO
- **Error Rate**: < 2%

### Logs Estruturados
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "service": "document-service",
  "event": "document_uploaded",
  "user_id": "uuid",
  "job_id": "uuid",
  "filename": "nota_fiscal.pdf",
  "file_size": 2048000,
  "mime_type": "application/pdf"
}
```

## 🧪 Testes

### Testes de Upload
```python
async def test_document_upload():
    """Testa upload de documento"""
    with open("test_document.pdf", "rb") as f:
        response = await client.post(
            "/upload",
            files={"file": f},
            headers={"Authorization": f"Bearer {token}"}
        )
    assert response.status_code == 200
    assert "job_id" in response.json()
```

### Testes de OCR
```python
async def test_ocr_processing():
    """Testa processamento OCR"""
    result = await process_ocr(file_content, "test.pdf")
    assert result.confidence > 0.8
    assert len(result.text) > 0
```

### Testes de Integração
```bash
# Upload de documento
curl -X POST http://localhost:8003/upload \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -F "file=@nota_fiscal.pdf"

# Verificar status
curl http://localhost:8003/jobs/$JOB_ID \
  -H "Authorization: Bearer $JWT_TOKEN"
```

## 🔒 Segurança

### Validações de Upload
- **File Type Validation**: Whitelist de tipos permitidos
- **Size Limits**: Máximo 10MB por arquivo
- **Virus Scanning**: (Futuro) Integração com ClamAV
- **User Isolation**: Arquivos separados por usuário

### Controle de Acesso
- **Authentication Required**: JWT obrigatório
- **User Scoping**: Usuários só acessam seus arquivos
- **Secure URLs**: URLs temporárias para download

### Considerações de Produção
- [ ] HTTPS obrigatório
- [ ] Virus scanning
- [ ] Backup automático
- [ ] Criptografia em trânsito
- [ ] Logs de auditoria

## 📊 Performance

### Otimizações Implementadas
- **Async Processing**: Upload não-bloqueante
- **Connection Pooling**: Para banco e MinIO
- **File Compression**: Para armazenamento
- **Batch Operations**: Para múltiplos arquivos

### Benchmarks Esperados
- **Upload Time**: < 2 segundos (arquivo 1MB)
- **OCR Processing**: < 10 segundos por página
- **Data Extraction**: < 5 segundos
- **Download Time**: < 1 segundo

## 🔄 Integração com Outros Serviços

### Auth Service
- Verifica tokens JWT
- Obtém user_id para isolamento

### Agent Orchestrator
- Recebe jobs de processamento
- Retorna dados extraídos
- Integração com LLMs especializados

### MinIO
- Armazenamento de arquivos
- Backup e versionamento
- URLs seguras para download

## 📈 Escalabilidade

### Horizontal Scaling
- **Stateless Design**: Sem estado local
- **Load Balancing**: Múltiplas instâncias
- **Queue System**: Redis/Celery para jobs

### Vertical Scaling
- **CPU**: Para processamento OCR
- **Memory**: Para cache de arquivos
- **Storage**: Para MinIO cluster

## 🔧 Tipos de Documento Suportados

### Notas Fiscais
```json
{
  "document_type": "nota_fiscal",
  "extracted_fields": {
    "cnpj_emitente": "string",
    "cnpj_destinatario": "string",
    "valor_total": "float",
    "data_emissao": "date",
    "descricao": "string",
    "numero_nota": "string",
    "serie": "string"
  }
}
```

### Recibos
```json
{
  "document_type": "recibo",
  "extracted_fields": {
    "valor": "float",
    "data": "date",
    "descricao": "string",
    "pagador": "string",
    "recebedor": "string"
  }
}
```

### Contratos
```json
{
  "document_type": "contrato",
  "extracted_fields": {
    "partes": ["string"],
    "valor": "float",
    "data_inicio": "date",
    "data_fim": "date",
    "objeto": "string"
  }
}
```

## 🚨 Tratamento de Erros

### Erros Comuns
- **File Too Large**: HTTP 400, mensagem específica
- **Invalid File Type**: HTTP 400, lista tipos permitidos
- **OCR Failure**: HTTP 500, retry automático
- **Storage Error**: HTTP 500, log detalhado

### Retry Logic
```python
async def process_document_with_retry(job_id: str, max_retries: int = 3):
    """Processa documento com retry automático"""
    for attempt in range(max_retries):
        try:
            return await process_document(job_id)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## 📋 Checklist de Produção

### Segurança
- [ ] HTTPS obrigatório
- [ ] Validação rigorosa de arquivos
- [ ] Isolamento por usuário
- [ ] Logs de auditoria

### Performance
- [ ] Cache de resultados
- [ ] Compressão de arquivos
- [ ] CDN para downloads
- [ ] Monitoramento de recursos

### Confiabilidade
- [ ] Backup automático
- [ ] Retry logic
- [ ] Health checks
- [ ] Alertas de erro


