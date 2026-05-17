from fastapi import (
    APIRouter,
    HTTPException
)

from backend.api.schema.scoring_schema import (
    CreditInput
)

from backend.ml.scoring.model import (
    predict_credit
)

# ========================
# Router
# ========================

router = APIRouter(

    prefix="/scoring",

    tags=["Credit Scoring"]
)

# ========================
# Endpoint
# ========================

@router.post("/predict")

def predict(data: CreditInput):

    try:

        result = predict_credit(data)

        return {

            "success": True,

            "data": result
        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=f"Prediction error: {str(e)}"
        )