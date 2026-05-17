# ========================
# Imports
# ========================

from fastapi import APIRouter
from backend.api.schema.fraud_schema import (
    
    FraudRequest
)

from backend.ml.fraud.model import (
    
    predict_fraud
)
# ========================
# Router
# ========================

router = APIRouter()

# ========================
# Fraud Endpoint
# ========================

@router.post("/predict-fraud")

def fraud_prediction(
    
    request: FraudRequest
):
    
    prediction = (
        
        predict_fraud(
            
            request.model_dump()
        )
    )
    
    return prediction
