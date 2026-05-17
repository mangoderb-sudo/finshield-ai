# ========================
# Imports
# ========================

import streamlit as st
import pandas as pd

# ========================
# PAGE CONFIG
# ========================

st.set_page_config(
    page_title="FinShield AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ========================
# LOAD CREDIT DATA
# ========================

@st.cache_data
def load_credit_data():

    return pd.read_csv(
        "data/credit/application_train.csv"
    )


# ========================
# LOAD RISK DATA
# ========================

@st.cache_data
def load_risk_data():

    return pd.read_csv(
        "data/credit/risk_metrics.csv"
    )

# ========================
# DATA
# ========================

df = load_credit_data()

risk_df = load_risk_data()

# ========================
# KPIs
# ========================

total_exposure = (
    df["AMT_CREDIT"].sum()
)

avg_pd = (
    risk_df["predicted_pd"].mean()
)

avg_credit_score = (
    risk_df["credit_score"].mean()
)

npl_ratio = (

    (
        risk_df["decision"] == "Reject"
    ).mean()

) * 100

manual_review_queue = (

    risk_df["decision"]

    == "Manual Review"

).sum()


# ========================
# CSS
# ========================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL
    ===================================================== */

    .stApp {

        background:
        linear-gradient(
            135deg,
            #06111F 0%,
            #0B1728 45%,
            #132238 100%
        );

        color: white;

        font-family: 'Segoe UI', sans-serif;
    }

    header {
        visibility: hidden;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    div[data-testid="stSidebarNav"] {
        display: none;
    }
    /* =====================================================
       SIDEBAR
    ===================================================== */

    section[data-testid="stSidebar"] {

        background:
        linear-gradient(
            180deg,
            #081221 0%,
            #0E1B2E 100%
        );

        border-right:
        1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {

        color: white !important;
    }

    section[data-testid="stSidebar"] a {

        font-size: 18px !important;

        font-weight: 600 !important;

        border-radius: 12px;

        padding-top: 10px !important;

        padding-bottom: 10px !important;
    }

    section[data-testid="stSidebar"] a:hover {

        background-color:
        rgba(59,130,246,0.12);
    }
    /* =====================================================
       HEADERS
    ===================================================== */

    .main-title {

        font-size: 56px;

        font-weight: 800;

        color: white;

        margin-bottom: 10px;
    }

    .subtitle {

        color: #9FB3C8;

        font-size: 22px;

        margin-bottom: 35px;
    }

    .section-title {

        color: #60A5FA;

        font-size: 32px;

        font-weight: 800;

        margin-top: 25px;

        margin-bottom: 20px;
    }
    /* =====================================================
       EXECUTIVE CARDS
    ===================================================== */
    .executive-card {

        background:
        rgba(255,255,255,0.04);

        border:
        1px solid rgba(255,255,255,0.06);

        border-radius: 24px;

        padding: 28px;

        backdrop-filter: blur(10px);

        box-shadow:
        0 8px 30px rgba(0,0,0,0.30);

        transition: 0.3s ease;
    }

    .executive-card:hover {

        transform: translateY(-5px);

        border:
        1px solid rgba(96,165,250,0.30);
    }

    .executive-title {

        color: white;

        font-size: 24px;

        font-weight: 700;

        margin-bottom: 15px;
    }

    .executive-text {

        color: #CBD5E1;

        font-size: 16px;

        line-height: 1.8;
    }
    /* =====================================================
       KPI CARDS
    ===================================================== */
    .kpi-card {

        background:
        rgba(255,255,255,0.04);

        border:
        1px solid rgba(255,255,255,0.06);

        border-radius: 24px;

        padding: 28px;

        backdrop-filter: blur(10px);

        box-shadow:
        0 8px 30px rgba(0,0,0,0.30);

        transition: 0.3s ease;
    }

    .kpi-label {

        color: #94A3B8;

        font-size: 15px;

        margin-bottom: 10px;
    }

    .kpi-value {

        color: white;

        font-size: 42px;

        font-weight: 800;
    }

    .kpi-trend-up {

        color: #10B981;

        font-size: 15px;

        font-weight: 600;

        margin-top: 8px;
    }

    .kpi-trend-warning {

        color: #F59E0B;

        font-size: 15px;

        font-weight: 600;

        margin-top: 8px;
    }
    /* =====================================================
       RISK PANEL
    ===================================================== */

    .risk-panel {

        background:
        rgba(255,255,255,0.04);

        border-radius: 24px;

        padding: 28px;

        border:
        1px solid rgba(255,255,255,0.08);
    }

    .risk-title {

        font-size: 24px;

        font-weight: 700;

        margin-bottom: 20px;
    }

    .risk-item {

        display: flex;

        justify-content: space-between;

        margin-bottom: 18px;

        padding-bottom: 12px;

        border-bottom:
        1px solid rgba(255,255,255,0.05);
    }

    .risk-name {

        color: #CBD5E1;

        font-size: 16px;
    }

    .risk-value-green {

        color: #10B981;

        font-weight: 700;
    }

    .risk-value-orange {

        color: #F59E0B;

        font-weight: 700;
    }

    .risk-value-red {

        color: #EF4444;

        font-weight: 700;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ========================
# SIDEBAR
# ========================

with st.sidebar:

    st.markdown("# 🏦 FinShield AI")

    st.caption(
        "Enterprise Banking Intelligence"
    )

    st.markdown("---")

    st.page_link(
        "app.py",
        label="📊 Executive Dashboard"
    )

    st.page_link(
        "pages/scoring.py",
        label="💳 Credit Scoring"
    )

    st.page_link(
        "pages/fraude.py",
        label="🚨 Fraud Monitoring"
    )

    st.page_link(
        "pages/assistant.py",
        label="🤖 AI Assistant"
    )

    st.markdown("---")

    st.success("Core Banking Systems Operational")


# ========================
# HEADER
# ========================

st.markdown(
    '<div class="main-title">🏦 FinShield AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div class="subtitle">
    Enterprise Financial Risk Intelligence & Decision Platform
    </div>
    ''',
    unsafe_allow_html=True
)
# ========================
# KPI ROW
# ========================

k1, k2, k3 = st.columns(3)

with k1:

    st.markdown(
        f"""<div class="kpi-card">

<div class="kpi-label">
Portfolio Exposure
</div>

<div class="kpi-value">
${total_exposure/1_000_000:.1f}M
</div>

<div class="kpi-trend-up">
▲ +4.2% this month
</div>

</div>""",
        unsafe_allow_html=True
    )

with k2:

    st.markdown(
        f"""<div class="kpi-card">

<div class="kpi-label">
Average Risk Score
</div>

<div class="kpi-value">
{avg_credit_score:.0f}
</div>

<div class="kpi-trend-up">
Stable portfolio quality
</div>

</div>""",
        unsafe_allow_html=True
    )

with k3:

    st.markdown(
        """<div class="kpi-card">

<div class="kpi-label">
Active Models
</div>

<div class="kpi-value">
3
</div>

<div class="kpi-trend-up">
All systems operational
</div>

</div>""",
        unsafe_allow_html=True
    )

# ========================
# PLATFORM MODULES
# ========================

st.markdown(
    '<div class="section-title">📊 Banking Intelligence Modules</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """<div class="executive-card">

<div class="executive-title">
💳 Credit Risk Assessment
</div>

<div class="executive-text">
Advanced borrower risk scoring powered by
XGBoost, calibrated probability estimation,
engineered financial ratios and SHAP explainability.

Supports underwriting automation,
portfolio segmentation and default risk analysis.
</div>

</div>""",
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """<div class="executive-card">

<div class="executive-title">
🚨 Fraud Monitoring Engine
</div>

<div class="executive-text">
Real-time transaction surveillance designed
to identify suspicious payment behavior,
transaction anomalies and operational fraud signals.
</div>

</div>""",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        """<div class="executive-card">

<div class="executive-title">
🤖 Financial AI Assistant
</div>

<div class="executive-text">
Retrieval-Augmented Generation assistant
connected to underwriting policies,
risk documentation and explainability knowledge bases.
</div>

</div>""",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """<div class="executive-card">
<div class="executive-title">⚡ Real-Time Decision APIs</div>
<div class="executive-text">Enterprise-grade FastAPI architecture supporting scalable machine learning inference for financial institutions.</div>
</div>""",
        unsafe_allow_html=True
    )
# ========================
# RISK PANEL
# ========================

st.markdown(
    '''<div class="section-title">📉 Portfolio Risk Summary</div>''',
    unsafe_allow_html=True
)

st.markdown(
    f"""<div class="risk-panel">

<div class="risk-title">Current Portfolio Indicators</div>

<div class="risk-item">
<div class="risk-name">Non-Performing Loans Ratio</div>

<div class="risk-value-orange">{npl_ratio:.1f}%</div>
</div>

<div class="risk-item">

<div class="risk-name">Average Probability of Default</div>
<div class="risk-value-green">{avg_pd:.1%}</div>
</div>

<div class="risk-item">
<div class="risk-name">Manual Review Queue</div>

<div class="risk-value-orange">{manual_review_queue}</div>
</div>

<div class="risk-item">
<div class="risk-name">Fraud Detection Confidence</div>

<div class="risk-value-green">82.6</div>
</div>

<div class="risk-item">

<div class="risk-name">Explainability Coverage</div>

<div class="risk-value-green">SHAP Enabled</div>

</div>

</div>""",
    unsafe_allow_html=True
)
# ========================
# FOOTER
# ========================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("---")

footer_col1, footer_col2, footer_col3 = st.columns([2,1,1])

with footer_col1:

    st.caption(
        "FinShield AI · Enterprise Banking Risk Intelligence Platform"
    )

with footer_col2:

    st.caption(
        "Version 1.0"
    )

with footer_col3:

    st.caption(
        "Powered by FastAPI · XGBoost · Mistral AI"
    )


# ========================
# OPTIONAL ALERTS
# ========================

st.markdown(
    '<div class="section-title">🔔 Operational Alerts</div>',
    unsafe_allow_html=True
)

alert_col1, alert_col2 = st.columns(2)

with alert_col1:

    st.markdown(
        """<div class="executive-card">

<div class="executive-title">
⚠️ Credit Monitoring
</div>

<div class="executive-text">

12 applications require additional
underwriting verification due to elevated
debt-to-income ratios.

</div>

</div>""",
        unsafe_allow_html=True
    )
with alert_col2:

    st.markdown(
        """<div class="executive-card">
<div class="executive-title">🚨 Fraud Surveillance</div>

<div class="executive-text">
Real-time fraud engine detected unusual
transaction velocity patterns across
3 payment accounts.
</div>

</div>""",
        unsafe_allow_html=True
    )


# ========================
# SYSTEM STATUS
# ========================

st.markdown(
    '<div class="section-title">🖥️ System Status</div>',
    unsafe_allow_html=True
)

sys1, sys2, sys3 = st.columns(3)

with sys1:

    st.markdown(
        """<div class="kpi-card">
<div class="kpi-label">API Gateway</div>

<div class="kpi-value">✅</div>
<div class="kpi-trend-up">Operational</div>
</div>""",

        unsafe_allow_html=True
    )

with sys2:

    st.markdown(
        """<div class="kpi-card">
<div class="kpi-label">Vector Database</div>
<div class="kpi-value">27</div>
<div class="kpi-trend-up">
Active RAG chunks
</div>
</div>""",
        unsafe_allow_html=True
    )

with sys3:

    st.markdown(
        """<div class="kpi-card">

<div class="kpi-label">Explainability</div>
<div class="kpi-value">SHAP</div>

<div class="kpi-trend-up">Enabled</div>

</div>""",
        unsafe_allow_html=True
    )
