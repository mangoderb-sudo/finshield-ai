from pathlib import Path

import joblib
import pandas as pd
import xgboost


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
print(pipeline)


# =====================================================
# FEATURE NAMES
# =====================================================

feature_names = (

    pipeline

    .named_steps["preprocessor"]

    .get_feature_names_out()
)


# =====================================================
# PREDICTION FUNCTION
# =====================================================

def predict_credit(data):

    # ==========================================
    # INPUT DATAFRAME
    # ==========================================

    df = pd.DataFrame([data.dict()])

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = pipeline.predict(df)[0]

    probability = (
        pipeline.predict_proba(df)[0][1]
    )

    # ==========================================
    # RISK LEVEL
    # ==========================================

    if probability >= 0.80:

        risk_level = "HIGH RISK"

    elif probability >= 0.50:

        risk_level = "MEDIUM RISK"

    else:

        risk_level = "LOW RISK"

    # ==========================================
    # FEATURE ENGINEERING
    # ==========================================

    df_engineered = (

       pipeline

       .named_steps["feature_engineering"]

       .transform(df)
    )

    # ==========================================
    # PREPROCESSING
    # ==========================================

    input_transformed = (

       pipeline

       .named_steps["preprocessor"]

       .transform(df_engineered)
    )

    # ==========================================
    # XGBOOST BOOSTER
    # ==========================================

    booster = (

        pipeline

        .named_steps["model"]

        .get_booster()
    )

    # ==========================================
    # SHAP CONTRIBUTIONS
    # ==========================================

    shap_values = booster.predict(

        xgboost.DMatrix(
            input_transformed
        ),

        pred_contribs=True
    )

    # ==========================================
    # FEATURE IMPORTANCE
    # ==========================================

    feature_importance = dict(

        zip(

            feature_names,

            shap_values[0][:-1]
        )
    )

    # ==========================================
    # TOP FEATURES
    # ==========================================

    top_features = sorted(

        feature_importance.items(),

        key=lambda x: abs(x[1]),

        reverse=True

    )[:5]

    # ==========================================
    # JSON SAFE
    # ==========================================

    top_features_clean = [

        (
            str(feature),

            float(value)
        )

        for feature, value in top_features
    ]

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "prediction":
            int(prediction),

        "default_probability":
            round(float(probability), 4),

        "risk_level":
            risk_level,

        "top_risk_factors":
            top_features_clean
    }
