# Credit Scoring System

## Overview

The credit scoring system is designed to estimate the probability that a borrower will default on a loan obligation. The model predicts the Probability of Default (PD) using machine learning techniques and engineered financial risk indicators.

## The scoring system supports:

loan approval decisions
borrower risk segmentation
portfolio risk management
explainable AI analysis
underwriting support

The system was developed using the Home Credit Default Risk dataset.

## Modeling Pipeline

The credit scoring pipeline includes:

Data preprocessing
Missing value handling
Feature engineering
Categorical encoding
Model training
Probability calibration
Threshold optimization
Risk segmentation
Explainability analysis

The final production model uses:

XGBoost classifier
CatBoostEncoder for categorical variables
probability calibration using sigmoid scaling
SHAP explainability
## Main Predictive Features

The model relies heavily on financial and behavioral risk indicators.

### External Risk Scores

The most important predictive variables are:

EXT_SOURCE_1
EXT_SOURCE_2
EXT_SOURCE_3

These external scores strongly influence borrower risk predictions.

Low EXT_SOURCE values generally increase default probability.

### Financial Ratio Features

Several engineered financial ratios improve risk detection:

CREDIT_INCOME_RATIO

Measures the relationship between total credit amount and borrower income.

High values indicate:

higher debt burden
reduced repayment capacity
elevated default risk
ANNUITY_INCOME_RATIO

Measures the proportion of borrower income consumed by loan annuity payments.

High values suggest:

financial pressure
repayment stress
increased credit risk
GOODS_CREDIT_RATIO

Measures the relationship between purchased goods value and granted credit amount.

### Employment and Stability Features
EMPLOYMENT_YEARS

Longer employment duration generally indicates:

greater financial stability
lower probability of default
EMPLOYMENT_INCOME_RATIO

Combines employment stability and income level.

### Demographic Features
AGE_YEARS

Older borrowers generally exhibit:

lower default probability
stronger repayment stability
YOUNG_CLIENT

Binary indicator identifying younger borrowers.

Young borrowers statistically exhibit higher default risk.

### Contact and Documentation Features
CONTACT_COMPLETENESS

Measures the availability of borrower contact information.

Low completeness may indicate:

weaker customer traceability
elevated operational risk
### DOCUMENT_COMPLETENESS

Measures the completeness of submitted borrower documents.

Incomplete documentation may increase underwriting uncertainty.

## Class Imbalance

The dataset is highly imbalanced.

Approximate class distribution:

non-default: ~92%
default: ~8%

The modeling pipeline accounts for imbalance using:

threshold optimization
recall-focused evaluation
calibrated probability analysis
## Model Evaluation Metrics

Several evaluation metrics are used.

### ROC-AUC

Measures the model's ability to rank risky borrowers above safer borrowers.

### Gini Coefficient

The Gini coefficient evaluates discriminatory power.

Higher Gini values indicate better separation between good and bad borrowers.

### Recall

Recall measures the proportion of actual defaults successfully detected.

High recall is important because:

missed defaults generate financial losses
false negatives are costly in lending environments
### Precision

Precision measures the reliability of predicted defaults.

## Threshold Optimization

The credit scoring system uses threshold optimization to balance:

borrower acceptance
default detection
operational cost

Lower thresholds:

increase recall
increase false positives

Higher thresholds:

reduce false positives
miss more defaults

The selected threshold balances business risk and customer acceptance.

## Probability Calibration

The model probabilities were calibrated using sigmoid calibration.

Calibration ensures:

predicted PD values better reflect true default probabilities
improved interpretability
more realistic risk segmentation
## Risk Bands

Borrowers are segmented into calibrated risk categories.

A — Low Risk

Characteristics:

very low predicted default probability
strong repayment profile
stable financial indicators

Typical decision:

automatic approval
B — Moderate Risk

Characteristics:

manageable default probability
acceptable financial stability

Typical decision:

approval with monitoring
C — High Risk

Characteristics:

elevated probability of default
weaker financial indicators
higher underwriting uncertainty

Typical decision:

manual review
D — Critical Risk

Characteristics:

very high predicted default probability
significant financial instability

Typical decision:

rejection
## Lending Decision Logic

The lending system uses risk-band-based underwriting logic.

Decision rules:

A → Approve
B → Approve
C → Manual Review
D → Reject

The system uses statistical risk estimation rather than deterministic prediction.

Some high-risk borrowers may still repay successfully. Some approved borrowers may still default.

The objective is to optimize overall portfolio risk.

## SHAP Explainability

SHAP values are used to explain borrower-level predictions.

SHAP analysis identifies:

which features increase borrower risk
which features reduce borrower risk
how financial indicators influence predictions

Examples of risk-increasing signals:

low EXT_SOURCE scores
high CREDIT_INCOME_RATIO
unstable employment
high annuity burden

Examples of risk-reducing signals:

long employment history
higher age
strong external scores
## Business Interpretation

The credit scoring system supports:

automated underwriting
portfolio monitoring
explainable risk assessment
lending decision support
risk segmentation

The system is intended to assist risk analysts rather than fully replace human underwriting.