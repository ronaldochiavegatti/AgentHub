-- AgentHub Platform Database Schemas
-- PostgreSQL schemas for microservices architecture

-- =============================================
-- AUTH SERVICE DATABASE
-- =============================================

CREATE DATABASE auth_service;
\c auth_service;

-- Users table
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

-- User sessions for JWT management
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_revoked BOOLEAN DEFAULT false
);

-- =============================================
-- AGENT ORCHESTRATOR DATABASE
-- =============================================

CREATE DATABASE agent_orchestrator;
\c agent_orchestrator;

-- Agents table - stores basic agent information
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL, -- 'accounting', 'legal', 'financial', etc.
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent capabilities - defines what each agent can do
CREATE TABLE agent_capabilities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    capability_type VARCHAR(50) NOT NULL, -- 'document_processing', 'chat', 'analysis'
    capability_name VARCHAR(100) NOT NULL,
    description TEXT,
    config_json JSONB NOT NULL, -- Contains prompts, RAG config, etc.
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent conversations for chat history
CREATE TABLE agent_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL, -- Reference to auth service user
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    session_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES agent_conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    tokens_used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Knowledge base for RAG (using pgvector extension)
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'document', 'faq', 'regulation'
    embedding vector(1536), -- For OpenAI embeddings
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for vector similarity search
CREATE INDEX ON knowledge_base USING ivfflat (embedding vector_cosine_ops);

-- =============================================
-- DOCUMENT SERVICE DATABASE
-- =============================================

CREATE DATABASE document_service;
\c document_service;

-- Document processing jobs
CREATE TABLE document_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'processing', 'completed', 'failed'
    ocr_result JSONB,
    extracted_data JSONB,
    error_message TEXT,
    processing_started_at TIMESTAMP,
    processing_completed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document processing results
CREATE TABLE document_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_id UUID REFERENCES document_jobs(id) ON DELETE CASCADE,
    result_type VARCHAR(50) NOT NULL, -- 'invoice_data', 'receipt_data', 'contract_analysis'
    extracted_fields JSONB NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- BILLING SERVICE DATABASE
-- =============================================

CREATE DATABASE billing_service;
\c billing_service;

-- User token balances
CREATE TABLE user_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    balance INTEGER DEFAULT 0,
    total_purchased INTEGER DEFAULT 0,
    total_used INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Token transactions
CREATE TABLE token_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- 'purchase', 'usage', 'refund'
    amount INTEGER NOT NULL, -- positive for purchase/refund, negative for usage
    service_type VARCHAR(50), -- 'chat', 'document_processing', 'analysis'
    agent_id UUID,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pricing configuration
CREATE TABLE pricing_config (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_type VARCHAR(50) NOT NULL,
    token_cost INTEGER NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- INITIAL DATA SETUP
-- =============================================

-- Insert default agents
\c agent_orchestrator;
INSERT INTO agents (name, description, category) VALUES 
('Agente Contábil', 'Especialista em contabilidade para MEI, processamento de documentos e declarações fiscais', 'accounting');

-- Insert agent capabilities
INSERT INTO agent_capabilities (agent_id, capability_type, capability_name, description, config_json) VALUES 
(
    (SELECT id FROM agents WHERE name = 'Agente Contábil'),
    'document_processing',
    'Processamento de Notas Fiscais',
    'Extrai dados estruturados de notas fiscais e documentos contábeis',
    '{
        "prompt": "Analise esta nota fiscal e extraia os seguintes dados: CNPJ do emitente, CNPJ do destinatário, valor total, data de emissão, descrição dos serviços/produtos. Retorne os dados em formato JSON estruturado.",
        "output_format": "json",
        "required_fields": ["cnpj_emitente", "cnpj_destinatario", "valor_total", "data_emissao", "descricao"]
    }'
),
(
    (SELECT id FROM agents WHERE name = 'Agente Contábil'),
    'chat',
    'Assistente MEI',
    'Responde dúvidas sobre declarações fiscais e obrigações do MEI',
    '{
        "rag_enabled": true,
        "knowledge_base": "mei_regulations",
        "system_prompt": "Você é um especialista contábil focado em Microempreendedores Individuais (MEI). Responda sempre com base na legislação brasileira atual e seja preciso em suas informações fiscais."
    }'
);

-- Insert pricing configuration
\c billing_service;
INSERT INTO pricing_config (service_type, token_cost, description) VALUES 
('chat', 10, 'Custo por mensagem no chat com agente'),
('document_processing', 50, 'Custo por processamento de documento via OCR'),
('analysis', 25, 'Custo por análise de documento');

