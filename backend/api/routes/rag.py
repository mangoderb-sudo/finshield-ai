# ========================
# Imports
# ========================

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.ml.rag.chain import (
    
    ask_rag
)

# ========================
# Request Schema
# ========================

class RAGRequest(
    
    BaseModel
):
    
    question: str

# ========================
# Router
# ========================

router = APIRouter()

# ========================
# Ask Endpoint
# ========================

@router.post("/ask")

def ask_question(
    
    request: RAGRequest
):
    try:
        response = (
            ask_rag(
                request.question
            )
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc)
        ) from exc
    
    return {
        
        "answer":
        response
    }
