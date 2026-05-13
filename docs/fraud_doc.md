# Fraud Detection System

The fraud detection system identifies suspicious financial transactions using both supervised machine learning and anomaly detection techniques.

The system is designed to:

detect fraudulent transactions
minimize missed fraud cases
reduce operational false alerts
identify anomalous transaction behavior
support explainable fraud monitoring

The fraud pipeline combines:

XGBoost supervised fraud classification
Isolation Forest anomaly detection
SHAP explainability
## Fraud Detection Objectives

Fraud detection differs from credit scoring.

Credit scoring predicts long-term repayment risk. Fraud detection identifies suspicious or malicious transaction behavior.

The primary business objective is:

maximize fraud detection recall
while controlling false alerts
## Dataset Characteristics

The fraud dataset is extremely imbalanced.

Approximate distribution:

legitimate transactions: ~99.83%
fraudulent transactions: ~0.17%

This severe imbalance makes fraud detection particularly challenging.

A model predicting all transactions as legitimate would achieve high accuracy while providing no operational value.

Therefore, metrics such as:

recall
precision
PR-AUC

are more important than simple accuracy.

## Feature Engineering
LOG_AMOUNT

A logarithmic transformation of transaction amount.

Purpose:

reduce skewness
stabilize distributions
improve model learning
HIGH_AMOUNT_FLAG

Binary feature identifying unusually large transactions.

High-value transactions statistically exhibit increased fraud risk.

Supervised Fraud Detection

The primary fraud model uses XGBoost classification.

The supervised model learns patterns associated with known fraud cases.

The system uses:

class imbalance weighting
threshold optimization
fraud-focused metrics
Fraud Threshold Optimization

Threshold optimization balances:

fraud detection sensitivity
operational false alerts

Lower thresholds:

detect more fraud
increase false positives

Higher thresholds:

reduce false alerts
miss more fraud cases

Operational thresholds are selected based on:

fraud cost
customer experience
risk tolerance
## Fraud Confusion Matrix Interpretation
### True Positives

Fraud correctly detected.

### False Positives

Legitimate transactions incorrectly flagged as fraud.

High false positives may:

frustrate customers
block legitimate payments
reduce customer trust
### False Negatives

Fraudulent transactions missed by the system.

False negatives represent the most critical business risk.

## Isolation Forest — Anomaly Detection

The system also includes Isolation Forest anomaly detection.

Purpose:

identify unusual transaction behavior
detect previously unseen fraud patterns
monitor anomalies without labels

Isolation Forest complements supervised fraud modeling.

The supervised model detects known fraud patterns. The anomaly model detects suspicious unknown behavior.

## Fraud Explainability

SHAP analysis explains fraud predictions.

The most influential fraud variables include:

V14
V4
V12
V10
Amount
Time

The PCA-transformed variables dominate predictive power because they encode complex hidden transaction behavior patterns.

SHAP explanations help analysts understand:

why a transaction was flagged
which variables increased fraud probability
how suspicious behavior patterns influence alerts
## Fraud Monitoring Workflow

Typical fraud workflow:

Transaction submitted
Fraud probability computed
Anomaly score evaluated
Threshold rules applied
Alert generated if suspicious
Manual review or automatic block triggered
## Business Interpretation

The fraud detection system supports:

transaction monitoring
fraud alerting
anomaly surveillance
explainable fraud investigation
operational fraud intelligence

The combined supervised and anomaly-based architecture improves robustness against evolving fraud strategies.