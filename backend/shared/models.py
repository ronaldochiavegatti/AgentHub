"""
Shared models and interfaces for AgentHub platform
"""
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class DocumentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class TransactionType(str, Enum):
    PURCHASE = "purchase"
    USAGE = "usage"
    REFUND = "refund"


class CapabilityType(str, Enum):
    DOCUMENT_PROCESSING = "document_processing"
    CHAT = "chat"
    ANALYSIS = "analysis"


# =============================================
# AUTH SERVICE MODELS
# =============================================

class UserBase(BaseModel):
    email: str = Field(..., description="User email address")
    first_name: str = Field(..., description="User first name")
    last_name: str = Field(..., description="User last name")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="User password")


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# =============================================
# AGENT ORCHESTRATOR MODELS
# =============================================

class AgentBase(BaseModel):
    name: str = Field(..., description="Agent name")
    description: Optional[str] = Field(None, description="Agent description")
    category: str = Field(..., description="Agent category")


class AgentCreate(AgentBase):
    pass


class AgentResponse(AgentBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CapabilityConfig(BaseModel):
    prompt: Optional[str] = None
    output_format: Optional[str] = None
    required_fields: Optional[List[str]] = None
    rag_enabled: Optional[bool] = False
    knowledge_base: Optional[str] = None
    system_prompt: Optional[str] = None


class AgentCapabilityBase(BaseModel):
    capability_type: CapabilityType
    capability_name: str
    description: Optional[str] = None
    config_json: CapabilityConfig


class AgentCapabilityCreate(AgentCapabilityBase):
    agent_id: uuid.UUID


class AgentCapabilityResponse(AgentCapabilityBase):
    id: uuid.UUID
    agent_id: uuid.UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChatMessage(BaseModel):
    role: str = Field(..., regex="^(user|assistant)$")
    content: str
    tokens_used: Optional[int] = 0


class ChatRequest(BaseModel):
    agent_id: uuid.UUID
    message: str
    session_id: Optional[uuid.UUID] = None


class ChatResponse(BaseModel):
    message: ChatMessage
    session_id: uuid.UUID
    tokens_used: int


class DocumentProcessingRequest(BaseModel):
    agent_id: uuid.UUID
    job_id: uuid.UUID
    document_url: str


class DocumentProcessingResponse(BaseModel):
    job_id: uuid.UUID
    extracted_data: Dict[str, Any]
    confidence_score: Optional[float] = None
    tokens_used: int


# =============================================
# DOCUMENT SERVICE MODELS
# =============================================

class DocumentJobBase(BaseModel):
    filename: str
    original_filename: str
    file_size: int
    mime_type: str


class DocumentJobCreate(DocumentJobBase):
    user_id: uuid.UUID
    file_path: str


class DocumentJobResponse(DocumentJobBase):
    id: uuid.UUID
    user_id: uuid.UUID
    file_path: str
    status: DocumentStatus
    ocr_result: Optional[Dict[str, Any]] = None
    extracted_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    processing_started_at: Optional[datetime] = None
    processing_completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    job_id: uuid.UUID
    filename: str
    status: DocumentStatus
    message: str


class OCRResult(BaseModel):
    text: str
    confidence: float
    bounding_boxes: Optional[List[Dict[str, Any]]] = None


class ExtractedData(BaseModel):
    document_type: str
    fields: Dict[str, Any]
    confidence_score: float


# =============================================
# BILLING SERVICE MODELS
# =============================================

class TokenBalance(BaseModel):
    user_id: uuid.UUID
    balance: int
    total_purchased: int
    total_used: int


class TokenTransactionBase(BaseModel):
    user_id: uuid.UUID
    transaction_type: TransactionType
    amount: int
    service_type: Optional[str] = None
    agent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None


class TokenTransactionCreate(TokenTransactionBase):
    pass


class TokenTransactionResponse(TokenTransactionBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class PricingConfig(BaseModel):
    service_type: str
    token_cost: int
    description: Optional[str] = None
    is_active: bool = True


class TokenUsageRequest(BaseModel):
    user_id: uuid.UUID
    service_type: str
    tokens_used: int
    agent_id: Optional[uuid.UUID] = None
    description: Optional[str] = None


class TokenPurchaseRequest(BaseModel):
    user_id: uuid.UUID
    amount: int
    payment_method: str


# =============================================
# KNOWLEDGE BASE MODELS
# =============================================

class KnowledgeItem(BaseModel):
    id: uuid.UUID
    agent_id: uuid.UUID
    title: str
    content: str
    content_type: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class KnowledgeSearchRequest(BaseModel):
    agent_id: uuid.UUID
    query: str
    limit: int = 5


class KnowledgeSearchResponse(BaseModel):
    items: List[KnowledgeItem]
    query: str
    total_results: int


# =============================================
# API RESPONSE MODELS
# =============================================

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    details: Optional[Dict[str, Any]] = None

