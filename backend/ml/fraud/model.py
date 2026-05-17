# ========================
# Imports
# ========================

import joblib
import pandas as pd

# ========================
# Load Fraud Model
# ========================

model = joblib.load(
    
    "backend/ml/fraud/fraud_model.pkl"
)

# ========================
# Load Features
# ========================

feature_columns = joblib.load(
    
    "backend/ml/fraud/features.pkl"
)

# ========================
# Fraud Prediction Function
# ========================

def predict_fraud(
    
    data
):
    
    # Convert to DataFrame
    input_df = pd.DataFrame(
        
        [data]
    )
    
    # Keep correct feature order
    input_df = input_df[
        
        feature_columns
    ]
    
    # Fraud probability
    fraud_probability = (
        
        model.predict_proba(
            
            input_df
        )[0][1]
    )
    
    # Risk logic
    if fraud_probability < 0.30:
        
        fraud_risk = (
            
            "Low Risk"
        )
        
        decision = (
            
            "Approved"
        )
    
    elif fraud_probability < 0.70:
        
        fraud_risk = (
            
            "Medium Risk"
        )
        
        decision = (
            
            "Manual Review"
        )
    
    else:
        
        fraud_risk = (
            
            "High Risk"
        )
        
        decision = (
            
            "Blocked"
        )
    
    return {
        
        "fraud_probability":
        round(float(fraud_probability), 4),
        
        "fraud_risk":
        fraud_risk,
        
        "decision":
        decision
    }