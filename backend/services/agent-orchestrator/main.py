"""
Agent Orchestrator Service - AgentHub Platform
Handles agent management, chat interactions, and RAG-based responses
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Text, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.sql import func
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import sys
import json
import httpx
import asyncio
import google.generativeai as genai

# Add shared models to path
sys.path.append('../../shared')
from models import (
    AgentResponse, AgentCapabilityResponse, ChatRequest, ChatResponse,
    ChatMessage, DocumentProcessingRequest, DocumentProcessingResponse,
    KnowledgeSearchRequest, KnowledgeSearchResponse, KnowledgeItem,
    APIResponse, ErrorResponse, CapabilityType
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/agent_orchestrator")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentCapability(Base):
    __tablename__ = "agent_capabilities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), nullable=False)
    capability_type = Column(String(50), nullable=False)
    capability_name = Column(String(100), nullable=False)
    description = Column(Text)
    config_json = Column(JSONB, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentConversation(Base):
    __tablename__ = "agent_conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    agent_id = Column(UUID(as_uuid=True), nullable=False)
    session_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id = Column(UUID(as_uuid=True), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(50), nullable=False)
    embedding = Column(ARRAY(Float))  # Vector embedding
    metadata = Column(JSONB)
    created_at = Column(DateTime, default=datetime.utcnow)

# FastAPI app
app = FastAPI(
    title="AgentHub Agent Orchestrator",
    description="Agent orchestration service for AgentHub platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
BILLING_SERVICE_URL = os.getenv("BILLING_SERVICE_URL", "http://localhost:8004")

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication helper
async def verify_user_token(token: str) -> str:
    """Verify user token with auth service"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{AUTH_SERVICE_URL}/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return response.json()["data"]["user_id"]

# RAG Implementation
async def search_knowledge_base(agent_id: str, query: str, limit: int = 5, db: Session = None) -> List[Dict[str, Any]]:
    """Search knowledge base using vector similarity"""
    # For now, implement a simple text search
    # In production, use proper vector similarity search with pgvector
    
    knowledge_items = db.query(KnowledgeBase).filter(
        KnowledgeBase.agent_id == agent_id,
        KnowledgeBase.content.contains(query)
    ).limit(limit).all()
    
    return [
        {
            "id": str(item.id),
            "title": item.title,
            "content": item.content,
            "content_type": item.content_type
        }
        for item in knowledge_items
    ]

async def generate_rag_response(query: str, context: List[Dict[str, Any]], system_prompt: str = None) -> str:
    """Generate response using RAG with Gemini 2.5 Pro"""
    
    # Prepare context
    context_text = "\n\n".join([f"**{item['title']}**\n{item['content']}" for item in context])
    
    # System prompt
    if not system_prompt:
        system_prompt = "Você é um assistente especializado. Responda com base no contexto fornecido de forma precisa e útil."
    
    # Create the prompt for Gemini
    prompt = f"{system_prompt}\n\nContexto:\n{context_text}\n\nPergunta: {query}"
    
    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=500,
                temperature=0.7,
            )
        )
        
        return response.text
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

async def charge_tokens(user_id: str, tokens_used: int, service_type: str, agent_id: str = None):
    """Charge tokens via billing service"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BILLING_SERVICE_URL}/charge-tokens",
            json={
                "user_id": user_id,
                "service_type": service_type,
                "tokens_used": tokens_used,
                "agent_id": agent_id,
                "description": f"Chat interaction with agent"
            }
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Insufficient token balance"
            )

# API Routes
@app.get("/agents", response_model=List[AgentResponse])
async def get_agents(db: Session = Depends(get_db)):
    """Get all active agents"""
    agents = db.query(Agent).filter(Agent.is_active == True).all()
    return [AgentResponse.from_orm(agent) for agent in agents]

@app.get("/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: Session = Depends(get_db)):
    """Get specific agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse.from_orm(agent)

@app.get("/agents/{agent_id}/capabilities", response_model=List[AgentCapabilityResponse])
async def get_agent_capabilities(agent_id: str, db: Session = Depends(get_db)):
    """Get capabilities for a specific agent"""
    capabilities = db.query(AgentCapability).filter(
        AgentCapability.agent_id == agent_id,
        AgentCapability.is_active == True
    ).all()
    return [AgentCapabilityResponse.from_orm(cap) for cap in capabilities]

@app.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    chat_request: ChatRequest,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Chat with an agent using RAG"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    # Get agent and chat capability
    agent = db.query(Agent).filter(Agent.id == chat_request.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    chat_capability = db.query(AgentCapability).filter(
        AgentCapability.agent_id == chat_request.agent_id,
        AgentCapability.capability_type == "chat",
        AgentCapability.is_active == True
    ).first()
    
    if not chat_capability:
        raise HTTPException(status_code=400, detail="Agent does not support chat")
    
    # Search knowledge base
    context = await search_knowledge_base(
        str(chat_request.agent_id),
        chat_request.message,
        db=db
    )
    
    # Generate response
    config = chat_capability.config_json
    system_prompt = config.get("system_prompt") if isinstance(config, dict) else None
    
    response_content = await generate_rag_response(
        chat_request.message,
        context,
        system_prompt
    )
    
    # Estimate tokens used (rough calculation)
    tokens_used = len(chat_request.message.split()) + len(response_content.split())
    
    # Charge tokens
    await charge_tokens(
        user_id,
        tokens_used,
        "chat",
        str(chat_request.agent_id)
    )
    
    # Create conversation and messages
    session_id = chat_request.session_id or uuid.uuid4()
    
    conversation = AgentConversation(
        user_id=user_id,
        agent_id=chat_request.agent_id,
        session_id=session_id
    )
    db.add(conversation)
    db.flush()
    
    # Save user message
    user_message = ChatMessage(
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message,
        tokens_used=len(chat_request.message.split())
    )
    db.add(user_message)
    
    # Save assistant message
    assistant_message = ChatMessage(
        conversation_id=conversation.id,
        role="assistant",
        content=response_content,
        tokens_used=len(response_content.split())
    )
    db.add(assistant_message)
    
    db.commit()
    
    return ChatResponse(
        message=ChatMessage(
            role="assistant",
            content=response_content,
            tokens_used=tokens_used
        ),
        session_id=session_id,
        tokens_used=tokens_used
    )

@app.post("/process-document", response_model=DocumentProcessingResponse)
async def process_document(
    request: DocumentProcessingRequest,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Process document using agent capabilities"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    # Get agent and document processing capability
    agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    doc_capability = db.query(AgentCapability).filter(
        AgentCapability.agent_id == request.agent_id,
        AgentCapability.capability_type == "document_processing",
        AgentCapability.is_active == True
    ).first()
    
    if not doc_capability:
        raise HTTPException(status_code=400, detail="Agent does not support document processing")
    
    # For now, return mock extracted data
    # In production, integrate with document service and OCR
    extracted_data = {
        "cnpj_emitente": "12.345.678/0001-90",
        "cnpj_destinatario": "98.765.432/0001-10",
        "valor_total": "1.500,00",
        "data_emissao": "2024-01-15",
        "descricao": "Serviços de consultoria contábil"
    }
    
    tokens_used = 50  # Estimated cost for document processing
    
    # Charge tokens
    await charge_tokens(
        user_id,
        tokens_used,
        "document_processing",
        str(request.agent_id)
    )
    
    return DocumentProcessingResponse(
        job_id=request.job_id,
        extracted_data=extracted_data,
        confidence_score=0.95,
        tokens_used=tokens_used
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "agent-orchestrator"}

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

