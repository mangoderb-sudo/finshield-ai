from pathlib import Path

import joblib
import pandas as pd


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

PIPELINE_PATH = (
    BASE_DIR / "scoring_pipeline.pkl"
)


# =====================================================
# LOAD PIPELINE
# =====================================================

pipeline = joblib.load(
    PIPELINE_PATH
)


# =====================================================
# PREDICTION FUNCTION
# =====================================================

def predict_credit(data):

    # convertir input → dataframe
    df = pd.DataFrame([data.dict()])

    # prediction classe
    prediction = pipeline.predict(df)[0]

    # probabilité défaut
    probability = (
        pipeline.predict_proba(df)[0][1]
    )

    # niveau risque
    if probability >= 0.80:

        risk_level = "HIGH RISK"

    elif probability >= 0.50:

        risk_level = "MEDIUM RISK"

    else:

        risk_level = "LOW RISK"

    return {

        "prediction":
            int(prediction),

        "default_probability":
            round(float(probability), 4),

        "risk_level":
            risk_level
    }