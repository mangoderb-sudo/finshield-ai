import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Financial AI Assistant",
    page_icon="AI",
    layout="wide"
)
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


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0B1120 0%, #111827 100%);
        color: white;
    }

    .title {
        color: white;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .subtitle {
        color: #9CA3AF;
        font-size: 18px;
        margin-bottom: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="title">Financial AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about your financial risk knowledge base.</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "Question",
    placeholder="Example: What factors increase credit default risk?",
    height=140
)

ask_button = st.button(
    "Ask Assistant",
    use_container_width=True
)

if ask_button:
    
    if not question.strip():
        
        st.warning(
            "Please enter a question first."
        )
    
    else:
        
        try:
            
            response = requests.post(
                
                f"{API_BASE_URL}/ask",
                
                json={
                    "question": question
                },
                
            )

            

            # Try JSON safely
            try:
                
                result = response.json()

                st.markdown(
                    "### 🤖 Assistant Answer"
                )

                st.success(
                    result.get(
                        "answer",
                        "No answer returned."
                    )
                )

            except Exception:
                
                st.error(
                    "Response is not valid JSON."
                )

        except Exception as exc:
            
            st.error(
                f"API Error: {exc}"
            )
    
