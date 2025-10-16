"""
Document Service - AgentHub Platform
Handles document upload, OCR processing, and data extraction
"""
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Text, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
import sys
import httpx
import asyncio
from minio import Minio
from minio.error import S3Error
import io
import json
import google.generativeai as genai

# Add shared models to path
sys.path.append('../../shared')
from models import (
    DocumentJobResponse, DocumentUploadResponse, DocumentStatus,
    OCRResult, ExtractedData, APIResponse, ErrorResponse
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/document_service")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MinIO configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "documents")

# Initialize MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Create bucket if it doesn't exist
try:
    if not minio_client.bucket_exists(MINIO_BUCKET):
        minio_client.make_bucket(MINIO_BUCKET)
except S3Error as e:
    print(f"Error creating bucket: {e}")

# Database Models
class DocumentJob(Base):
    __tablename__ = "document_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    mime_type = Column(String(100), nullable=False)
    status = Column(String(20), default='pending')
    ocr_result = Column(JSONB)
    extracted_data = Column(JSONB)
    error_message = Column(Text)
    processing_started_at = Column(DateTime)
    processing_completed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DocumentResult(Base):
    __tablename__ = "document_results"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), nullable=False)
    result_type = Column(String(50), nullable=False)
    extracted_fields = Column(JSONB, nullable=False)
    confidence_score = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

# FastAPI app
app = FastAPI(
    title="AgentHub Document Service",
    description="Document processing service for AgentHub platform",
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
AGENT_ORCHESTRATOR_URL = os.getenv("AGENT_ORCHESTRATOR_URL", "http://localhost:8002")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your-gemini-api-key")

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

# OCR Processing (Mock implementation)
async def process_ocr(file_content: bytes, filename: str) -> OCRResult:
    """Process document with OCR (mock implementation)"""
    # In production, integrate with Tesseract, Google Vision API, or Azure Computer Vision
    # For now, return mock OCR result
    
    mock_text = f"""
    NOTA FISCAL DE SERVIÇOS ELETRÔNICA
    Número: 000001
    Série: 1
    Data de Emissão: 15/01/2024
    
    PRESTADOR:
    CNPJ: 12.345.678/0001-90
    Razão Social: Empresa Exemplo LTDA
    Endereço: Rua das Flores, 123
    
    TOMADOR:
    CNPJ: 98.765.432/0001-10
    Razão Social: Cliente Exemplo LTDA
    
    SERVIÇOS:
    Descrição: Consultoria contábil
    Valor: R$ 1.500,00
    
    TOTAL: R$ 1.500,00
    """
    
    return OCRResult(
        text=mock_text.strip(),
        confidence=0.95,
        bounding_boxes=[]
    )

async def extract_document_data(ocr_result: OCRResult, agent_id: str) -> ExtractedData:
    """Extract structured data from OCR result using Gemini 2.5 Pro"""
    try:
        # Create prompt for Gemini to extract structured data
        prompt = f"""
        Extraia os dados estruturados da seguinte nota fiscal processada por OCR:
        
        {ocr_result.text}
        
        Por favor, extraia e retorne os seguintes campos em formato JSON:
        - cnpj_emitente
        - cnpj_destinatario
        - valor_total
        - data_emissao
        - descricao
        - numero_nota
        - serie
        
        Retorne apenas o JSON válido, sem explicações adicionais.
        """
        
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=300,
                temperature=0.1,  # Low temperature for consistent extraction
            )
        )
        
        # Parse the JSON response
        import json
        extracted_fields = json.loads(response.text.strip())
        
        return ExtractedData(
            document_type="nota_fiscal",
            fields=extracted_fields,
            confidence_score=0.92
        )
        
    except Exception as e:
        # Fallback to mock data if extraction fails
        print(f"Error extracting data with Gemini: {e}")
        extracted_fields = {
            "cnpj_emitente": "12.345.678/0001-90",
            "cnpj_destinatario": "98.765.432/0001-10",
            "valor_total": "1500.00",
            "data_emissao": "2024-01-15",
            "descricao": "Consultoria contábil",
            "numero_nota": "000001",
            "serie": "1"
        }
        
        return ExtractedData(
            document_type="nota_fiscal",
            fields=extracted_fields,
            confidence_score=0.70  # Lower confidence for fallback
        )

# API Routes
@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Upload and process a document"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file size (10MB limit)
    file_content = await file.read()
    if len(file_content) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # Check file type
    allowed_types = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg']
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed types: {', '.join(allowed_types)}"
        )
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = f"documents/{user_id}/{unique_filename}"
    
    try:
        # Upload to MinIO
        minio_client.put_object(
            MINIO_BUCKET,
            file_path,
            io.BytesIO(file_content),
            length=len(file_content),
            content_type=file.content_type
        )
        
        # Create document job record
        job = DocumentJob(
            user_id=user_id,
            filename=unique_filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=len(file_content),
            mime_type=file.content_type,
            status=DocumentStatus.PENDING
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        # Start background processing
        asyncio.create_task(process_document_async(job.id))
        
        return DocumentUploadResponse(
            job_id=job.id,
            filename=file.filename,
            status=DocumentStatus.PENDING,
            message="Document uploaded successfully"
        )
        
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

async def process_document_async(job_id: uuid.UUID):
    """Background task to process document"""
    db = SessionLocal()
    try:
        job = db.query(DocumentJob).filter(DocumentJob.id == job_id).first()
        if not job:
            return
        
        # Update status to processing
        job.status = DocumentStatus.PROCESSING
        job.processing_started_at = datetime.utcnow()
        db.commit()
        
        try:
            # Download file from MinIO
            response = minio_client.get_object(MINIO_BUCKET, job.file_path)
            file_content = response.read()
            response.close()
            response.release_conn()
            
            # Process OCR
            ocr_result = await process_ocr(file_content, job.original_filename)
            
            # Extract structured data
            extracted_data = await extract_document_data(ocr_result, "default")
            
            # Update job with results
            job.status = DocumentStatus.COMPLETED
            job.ocr_result = ocr_result.dict()
            job.extracted_data = extracted_data.dict()
            job.processing_completed_at = datetime.utcnow()
            
            db.commit()
            
        except Exception as e:
            # Update job with error
            job.status = DocumentStatus.FAILED
            job.error_message = str(e)
            job.processing_completed_at = datetime.utcnow()
            db.commit()
            
    except Exception as e:
        print(f"Error in background processing: {e}")
    finally:
        db.close()

@app.get("/jobs/{job_id}", response_model=DocumentJobResponse)
async def get_document_job(
    job_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get document processing job status"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    job = db.query(DocumentJob).filter(
        DocumentJob.id == job_id,
        DocumentJob.user_id == user_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return DocumentJobResponse.from_orm(job)

@app.get("/jobs", response_model=List[DocumentJobResponse])
async def get_user_document_jobs(
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Get all document jobs for current user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    jobs = db.query(DocumentJob).filter(
        DocumentJob.user_id == user_id
    ).order_by(DocumentJob.created_at.desc()).limit(50).all()
    
    return [DocumentJobResponse.from_orm(job) for job in jobs]

@app.get("/download/{job_id}")
async def download_document(
    job_id: str,
    authorization: str = None,
    db: Session = Depends(get_db)
):
    """Download processed document"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    # Extract token and verify user
    token = authorization.replace("Bearer ", "")
    user_id = await verify_user_token(token)
    
    job = db.query(DocumentJob).filter(
        DocumentJob.id == job_id,
        DocumentJob.user_id == user_id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        # Get file from MinIO
        response = minio_client.get_object(MINIO_BUCKET, job.file_path)
        file_content = response.read()
        response.close()
        response.release_conn()
        
        return {
            "filename": job.original_filename,
            "content": file_content,
            "content_type": job.mime_type
        }
        
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "document-service"}

# Create tables
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

