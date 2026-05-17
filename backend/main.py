# ========================
# FastAPI Imports
# ========================

from fastapi import FastAPI

from backend.api.routes.scoring import (
    router as scoring_router
)

from backend.api.routes.fraud import (
    router as fraud_router
)

from backend.api.routes.rag import ( 
    router as rag_router
)

# ========================
# Create App
# ========================

app = FastAPI(
    
    title="FinShield AI",
    
    version="1.0.0"
)

# ========================
# Root Endpoint
# ========================

@app.get("/")

def root():
    
    return {
        
        "message":
        "FinShield AI API is running."
    }

# ========================
# Health Endpoint
# ========================

@app.get("/health")

def health():
    
    return {
        
        "status":
        "healthy"
    }

# ========================
# Register Routes
# ========================

app.include_router(
    
    scoring_router
)

app.include_router(
    
    fraud_router
)

app.include_router(
    
    rag_router
)