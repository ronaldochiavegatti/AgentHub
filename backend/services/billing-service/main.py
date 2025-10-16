"""
Billing Service - AgentHub Platform
Handles token management, billing, and usage tracking
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import sys
import httpx

# Add shared models to path
sys.path.append('../../shared')
from models import (
    TokenBalance, TokenTransactionResponse, TokenTransactionCreate,
    TokenUsageRequest, TokenPurchaseRequest, PricingConfig,
    APIResponse, ErrorResponse, TransactionType
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/billing_service")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class UserTokens(Base):
    __tablename__ = "user_tokens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)
    balance = Column(Integer, default=0)
    total_purchased = Column(Integer, default=0)
    total_used = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TokenTransaction(Base):
    __tablename__ = "token_transactions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    transaction_type = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    service_type = Column(String(50))
    agent_id = Column(UUID(as_uuid=True))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class PricingConfig(Base):
    __tablename__ = "pricing_config"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_type = Column(String(50), nullable=False)
    token_cost = Column(Integer, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# FastAPI app
app = FastAPI(
    title="AgentHub Billing Service",
    description="Billing and token management service for AgentHub platform",
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
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")

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

def get_or_create_user_tokens(user_id: str, db: Session) -> UserTokens:
    """Get or create user tokens record"""
    user_tokens = db.query(UserTokens).filter(UserTokens.user_id == user_id).first()
    if not user_tokens:
        user_tokens = UserTokens(user_id=user_id, balance=1000)  # Give new users 1000 free tokens
        db.add(user_tokens)
        db.commit()
        db.refresh(user_tokens)
    return user_tokens

def get_pricing_config(service_type: str, db: Session) -> int:
    """Get pricing configuration for service type"""
    pricing = db.query(PricingConfig).filter(
        PricingConfig.service_type == service_type,
        PricingConfig.is_active == True
    ).first()
    
    if not pricing:
        return 10  # Default cost
    
    return pricing.token_cost

# API Routes
@app.get("/balance/{user_id}", response_model=TokenBalance)
async def get_user_token_balance(
    user_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get user token balance"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    verified_user_id = await verify_user_token(token)
    
    # Verify user can access this balance
    if verified_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_tokens = get_or_create_user_tokens(user_id, db)
    
    return TokenBalance(
        user_id=user_id,
        balance=user_tokens.balance,
        total_purchased=user_tokens.total_purchased,
        total_used=user_tokens.total_used
    )

@app.post("/charge-tokens", response_model=APIResponse)
async def charge_tokens(
    request: TokenUsageRequest,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Charge tokens for service usage"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    verified_user_id = await verify_user_token(token)
    
    # Verify user can charge these tokens
    if verified_user_id != request.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_tokens = get_or_create_user_tokens(request.user_id, db)
    
    # Check if user has enough tokens
    if user_tokens.balance < request.tokens_used:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Insufficient token balance"
        )
    
    # Deduct tokens
    user_tokens.balance -= request.tokens_used
    user_tokens.total_used += request.tokens_used
    
    # Create transaction record
    transaction = TokenTransaction(
        user_id=request.user_id,
        transaction_type=TransactionType.USAGE,
        amount=-request.tokens_used,  # Negative for usage
        service_type=request.service_type,
        agent_id=request.agent_id,
        description=request.description or f"Usage of {request.service_type}"
    )
    
    db.add(transaction)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Tokens charged successfully",
        data={
            "new_balance": user_tokens.balance,
            "tokens_used": request.tokens_used
        }
    )

@app.post("/purchase-tokens", response_model=APIResponse)
async def purchase_tokens(
    request: TokenPurchaseRequest,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Purchase tokens (mock implementation)"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    verified_user_id = await verify_user_token(token)
    
    # Verify user can purchase tokens
    if verified_user_id != request.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    user_tokens = get_or_create_user_tokens(request.user_id, db)
    
    # Add tokens to balance
    user_tokens.balance += request.amount
    user_tokens.total_purchased += request.amount
    
    # Create transaction record
    transaction = TokenTransaction(
        user_id=request.user_id,
        transaction_type=TransactionType.PURCHASE,
        amount=request.amount,
        description=f"Token purchase via {request.payment_method}"
    )
    
    db.add(transaction)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Tokens purchased successfully",
        data={
            "new_balance": user_tokens.balance,
            "tokens_purchased": request.amount
        }
    )

@app.get("/transactions/{user_id}", response_model=List[TokenTransactionResponse])
async def get_user_transactions(
    user_id: str,
    authorization: str = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get user transaction history"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    verified_user_id = await verify_user_token(token)
    
    # Verify user can access transactions
    if verified_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    transactions = db.query(TokenTransaction).filter(
        TokenTransaction.user_id == user_id
    ).order_by(TokenTransaction.created_at.desc()).limit(limit).all()
    
    return [TokenTransactionResponse.from_orm(txn) for txn in transactions]

@app.get("/pricing", response_model=List[PricingConfig])
async def get_pricing_configs(db: Session = Depends(get_db)):
    """Get current pricing configurations"""
    pricing_configs = db.query(PricingConfig).filter(
        PricingConfig.is_active == True
    ).all()
    
    return [PricingConfig.from_orm(config) for config in pricing_configs]

@app.post("/pricing", response_model=APIResponse)
async def create_pricing_config(
    config: PricingConfig,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Create new pricing configuration (admin only)"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # In production, verify admin permissions
    
    db_config = PricingConfig(
        service_type=config.service_type,
        token_cost=config.token_cost,
        description=config.description,
        is_active=config.is_active
    )
    
    db.add(db_config)
    db.commit()
    
    return APIResponse(
        success=True,
        message="Pricing configuration created successfully"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "billing-service"}

# Create tables and initial data
Base.metadata.create_all(bind=engine)

# Insert default pricing configurations
db = SessionLocal()
try:
    existing_configs = db.query(PricingConfig).count()
    if existing_configs == 0:
        default_configs = [
            PricingConfig(
                service_type="chat",
                token_cost=10,
                description="Custo por mensagem no chat com agente"
            ),
            PricingConfig(
                service_type="document_processing",
                token_cost=50,
                description="Custo por processamento de documento via OCR"
            ),
            PricingConfig(
                service_type="analysis",
                token_cost=25,
                description="Custo por análise de documento"
            )
        ]
        
        for config in default_configs:
            db.add(config)
        
        db.commit()
finally:
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)

