import streamlit as st
import requests
import plotly.graph_objects as go


# =====================================================
# CONFIG
# =====================================================

API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(

    page_title="FinShield AI",

    page_icon="🛡️",

    layout="wide"
)


# =====================================================
# CSS
# =====================================================

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
    
    .stApp {

        background:
        linear-gradient(
            135deg,
            #050816 0%,
            #0B1120 40%,
            #111827 100%
        );

        color: white;

        font-family: 'Segoe UI', sans-serif;
    }

    .main-title {

        font-size: 58px;

        font-weight: 800;

        color: white;

        margin-bottom: 5px;
    }

    .subtitle {

        color: white;

        font-size: 22px;

        margin-bottom: 30px;
    }

    /* STREAMLIT CARDS */

    div[data-testid="stVerticalBlock"] > div:has(div.element-container) {

        background: rgba(255,255,255,0.05);

        border: 1px solid rgba(255,255,255,0.08);

        backdrop-filter: blur(12px);

        border-radius: 24px;

        padding: 20px;

        margin-bottom: 20px;

        box-shadow:
        0 8px 32px rgba(0,0,0,0.35);
    }

    .big-score {

        font-size: 82px;

        font-weight: 800;

        text-align: center;

        color: white;
    }

    .risk-low {

        color: #10B981;

        font-size: 30px;

        font-weight: bold;

        text-align: center;
    }

    .risk-medium {

        color: #F59E0B;

        font-size: 30px;

        font-weight: bold;

        text-align: center;
    }

    .risk-high {

        color: #EF4444;

        font-size: 30px;

        font-weight: bold;

        text-align: center;
    }

    .approve {

        background:
        linear-gradient(
            135deg,
            #065F46,
            #10B981
        );

        padding: 18px;

        border-radius: 15px;

        text-align: center;

        font-size: 24px;

        font-weight: bold;

        color: white;

        margin-top: 20px;
    }

    .review {

        background:
        linear-gradient(
            135deg,
            #92400E,
            #F59E0B
        );

        padding: 18px;

        border-radius: 15px;

        text-align: center;

        font-size: 24px;

        font-weight: bold;

        color: white;

        margin-top: 20px;
    }

    .reject {

        background:
        linear-gradient(
            135deg,
            #7F1D1D,
            #EF4444
        );

        padding: 18px;

        border-radius: 15px;

        text-align: center;

        font-size: 24px;

        font-weight: bold;

        color: white;

        margin-top: 20px;
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



# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🛡️ FinShield AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '''
    <div class="subtitle">
    AI-Powered Credit Risk Intelligence Platform
    </div>
    ''',
    unsafe_allow_html=True
)


# =====================================================
# LAYOUT
# =====================================================

left_col, right_col = st.columns([1, 1])


# =====================================================
# LEFT PANEL
# =====================================================

with left_col:

    st.subheader("📋 Client Information")

    with st.expander(
        "💰 Financial Information",
        expanded=True
    ):

        income = st.number_input(
            "Annual Income",
            min_value=0.0,
            value=150000.0
        )

        credit = st.number_input(
            "Credit Amount",
            min_value=0.0,
            value=500000.0
        )

        annuity = st.number_input(
            "Annuity Amount",
            min_value=0.0,
            value=25000.0
        )

        goods_price = st.number_input(
            "Goods Price",
            min_value=0.0,
            value=450000.0
        )

    with st.expander(
        "👤 Personal Information",
        expanded=True
    ):

        age_years = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=35
        )

        employment_years = st.number_input(
            "Employment Years",
            min_value=0,
            max_value=50,
            value=5
        )

        children = st.number_input(
            "Children Count",
            min_value=0,
            max_value=10,
            value=0
        )

        gender = st.selectbox(
            "Gender",
            ["M", "F"]
        )

    with st.expander(
        "🎓 Professional Information",
        expanded=True
    ):

        education = st.selectbox(
            "Education Type",
            [
                "Higher education",
                "Secondary / secondary special",
                "Incomplete higher",
                "Lower secondary",
                "Academic degree"
            ]
        )

        income_type = st.selectbox(
            "Income Type",
            [
                "Working",
                "Commercial associate",
                "Pensioner",
                "State servant"
            ]
        )

        region_rating = st.selectbox(
            "Region Rating",
            [1, 2, 3]
        )

    with st.expander(
        "📊 External Scores",
        expanded=True
    ):

        ext1 = st.slider(
            "External Score 1",
            0.0,
            1.0,
            0.5
        )

        ext2 = st.slider(
            "External Score 2",
            0.0,
            1.0,
            0.5
        )

        ext3 = st.slider(
            "External Score 3",
            0.0,
            1.0,
            0.5
        )

    submitted = st.button(
        "🔍 Analyze Credit Risk",
        use_container_width=True
    )


# =====================================================
# RIGHT PANEL
# =====================================================

with right_col:


    if submitted:

        try:

            # ==========================================
            # CONVERT
            # ==========================================

            days_birth = -(age_years * 365)

            days_employed = -(
                employment_years * 365
            )

            # ==========================================
            # PAYLOAD
            # ==========================================

            payload = {

                "AMT_INCOME_TOTAL": income,

                "AMT_CREDIT": credit,

                "AMT_ANNUITY": annuity,

                "AMT_GOODS_PRICE": goods_price,

                "DAYS_BIRTH": days_birth,

                "DAYS_EMPLOYED": days_employed,

                "NAME_EDUCATION_TYPE":
                    education,

                "NAME_INCOME_TYPE":
                    income_type,

                "CODE_GENDER":
                    gender,

                "CNT_CHILDREN":
                    children,

                "REGION_RATING_CLIENT_W_CITY":
                    region_rating,

                "EXT_SOURCE_1":
                    ext1,

                "EXT_SOURCE_2":
                    ext2,

                "EXT_SOURCE_3":
                    ext3
            }

            # ==========================================
            # REQUEST
            # ==========================================

            response = requests.post(

                f"{API_BASE_URL}/scoring/predict",

                json=payload,

                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            prediction_data = result["data"]

            probability = prediction_data[
                "default_probability"
            ]

            risk_level = prediction_data[
                "risk_level"
            ]

            # ==========================================
            # SCORE
            # ==========================================

            st.markdown(

                f"""
                <div class="big-score">
                    {probability:.1%}
                </div>

                <p style="
                    text-align:center;
                    color:#9CA3AF;
                    font-size:18px;
                ">
                    Default Probability
                </p>
                """,

                unsafe_allow_html=True
            )

            # ==========================================
            # RISK
            # ==========================================

            if risk_level == "LOW RISK":

                risk_class = "risk-low"

                decision_class = "approve"

                decision_text = (
                    "✅ LOAN APPROVED"
                )

            elif risk_level == "MEDIUM RISK":

                risk_class = "risk-medium"

                decision_class = "review"

                decision_text = (
                    "⚠️ MANUAL REVIEW REQUIRED"
                )

            else:

                risk_class = "risk-high"

                decision_class = "reject"

                decision_text = (
                    "❌ LOAN REJECTED"
                )

            st.markdown(

                f"""
                <div class="{risk_class}">
                    {risk_level}
                </div>

                <div class="{decision_class}">
                    {decision_text}
                </div>
                """,

                unsafe_allow_html=True
            )

            # ==========================================
            # GAUGE
            # ==========================================

            fig = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=probability * 100,

                    title={
                        "text":
                        "Credit Risk Score"
                    },

                    gauge={

                        "axis": {
                            "range": [0, 100]
                        },

                        "bar": {
                            "color": "white"
                        },

                        "steps": [

                            {
                                "range": [0, 30],
                                "color": "#10B981"
                            },

                            {
                                "range": [30, 70],
                                "color": "#F59E0B"
                            },

                            {
                                "range": [70, 100],
                                "color": "#EF4444"
                            }
                        ]
                    }
                )
            )

            fig.update_layout(

                template="plotly_dark",

                height=320,

                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20
                ),

                paper_bgcolor=
                "rgba(0,0,0,0)",

                plot_bgcolor=
                "rgba(0,0,0,0)",

                font=dict(
                    color="white"
                )
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"API Error: {e}"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.caption(
    "FinShield AI · Credit Scoring · Fraud Detection · Explainable AI"
)