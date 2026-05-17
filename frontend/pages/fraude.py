import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

API_BASE_URL = "http://127.0.0.1:8000"

# ========================
# Page Config
# ========================

st.set_page_config(
    page_title="Fraud Monitoring",
    page_icon="🚨",
    layout="wide"
)

# ========================
# Custom CSS
# ========================

st.markdown(
    """
    <style>
    header {

    visibility: hidden;
    }

    [data-testid="stHeader"] {

      display: none;
    }
    /* Cache navigation automatique Streamlit */

    div[data-testid="stSidebarNav"] {

        display: none;
    }

    .stApp {
        background: linear-gradient(135deg, #0B1120 0%, #111827 100%);
        color: white;
    }
    
    section[data-testid="stSidebar"] {

      background:
      linear-gradient(
         180deg,
         #020617 0%,
         #0F172A 100%
      );

      border-right:
      1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {

        font-size: 22px !important;

       font-weight: 700 !important;

       color: white !important;

       padding-top: 5px !important;

       padding-bottom: 5px !important;

       border-radius: 12px;

       transition: 0.3s ease;
    }

    /* Sidebar logo/title */

    .sidebar-logo {

        font-size: 34px;

        font-weight: 800;

        text-align: center;

        margin-top: 10px;

        margin-bottom: 5px;

        color: white;
    }

    .sidebar-subtitle {

        text-align: center;

        color: #94A3B8;

        font-size: 15px;

        margin-bottom: 30px;
    }

    .title {
        font-size: 42px;
        font-weight: bold;
        color: white;
    }

    .subtitle {
        font-size: 18px;
        color: #9CA3AF;
        margin-bottom: 30px;
    }

    .fraud-alert {
        background-color: #991B1B;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }

    .safe-alert {
        background-color: #065F46;
        padding: 20px;
        border-radius: 14px;
        text-align: center;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }

    label {

    color: #93C5FD !important;

    font-size: 15px !important;

    font-weight: 700 !important;

    letter-spacing: 0.3px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
with st.sidebar:

    st.markdown("# 🛡️ FinShield AI")

    st.caption(
        "AI Financial Intelligence Platform"
    )

    st.markdown("---")

    st.page_link(
        "app.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/scoring.py",
        label="📈 Credit Scoring"
    )

    st.page_link(
        "pages/fraude.py",
        label="🚨 Fraud Detection"
    )

    st.page_link(
        "pages/assistant.py",
        label="🤖 AI Assistant"
    )


    st.markdown("---")

    st.info(
        "FinShield AI v1.0"
    )

# ========================
# Header
# ========================

st.markdown(
    '<div class="title">🚨 Fraud Monitoring System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Transaction Fraud Detection</div>',
    unsafe_allow_html=True
)
# Layout
# ========================

left_col, right_col = st.columns([1, 1])

# ========================
# Input Section
# ========================

with left_col:
    st.markdown("## 💳 Transaction Information")

    amount = st.number_input(
        "Transaction Amount",
        min_value=0.0,
        value=250.0,
        step=10.0
    )

    time = st.slider(
        "Transaction Time",
        min_value=0,
        max_value=172800,
        value=50000
    )

    st.markdown("---")
    st.markdown("## 🔬 PCA Fraud Features Simulation")

    st.caption(
        "The original fraud dataset contains anonymized PCA features (V1-V28)."
    )

    # Generate sliders dynamically
    fraud_inputs = {}
    for i in range(1, 29):

        fraud_inputs[f"V{i}"] = st.slider(
            f"V{i}",
            min_value=-10.0,
            max_value=10.0,
            value=0.0,
            step=0.1
        )

    predict_button = st.button(
        "🚀 Run Fraud Detection",
        use_container_width=True
    )


# ========================
# Prediction Section
# ========================

with right_col:

    st.markdown("## 📊 Fraud Prediction")

    if predict_button:

        payload = {
            "Time": float(time),
            "Amount": float(amount),
            "LOG_AMOUNT": float(np.log1p(amount)),
            "HIGH_AMOUNT_FLAG": int(amount > 365)
        }

        # Add PCA variables
        for i in range(1, 29):
            payload[f"V{i}"] = fraud_inputs[f"V{i}"]

        try:

            response = requests.post(
                f"{API_BASE_URL}/predict-fraud",
                json=payload,
            )

            response.raise_for_status()

            result = response.json()

            fraud_probability = result["fraud_probability"]
            fraud_risk = result["fraud_risk"]
            decision = result["decision"]

            # Metrics
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Fraud Probability",
                    value=f"{fraud_probability:.2%}"
                )

            with col2:
                st.metric(
                    label="Risk Level",
                    value=fraud_risk
                )

            st.markdown("### 🧠 Fraud Decision")

            if decision == "Blocked":
                st.markdown(
                    '<div class="fraud-alert">🚨 TRANSACTION BLOCKED</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="safe-alert">✅ TRANSACTION APPROVED</div>',
                    unsafe_allow_html=True
                )

            # Gauge Chart
            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=fraud_probability * 100,
                    title={"text": "Fraud Risk %"},
                    gauge={
                        "axis": {"range": [0, 100]},
                        "bar": {"color": "white"},
                        "steps": [
                            {"range": [0, 30], "color": "green"},
                            {"range": [30, 70], "color": "orange"},
                            {"range": [70, 100], "color": "red"}
                        ]
                    }
                )
            )
            fig.update_layout(
                height=350,
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"API Error: {e}"
            )
# ========================
# Footer
# ========================

st.markdown("---")

st.caption(
    "FinShield AI · Real-Time Fraud Monitoring"
)
