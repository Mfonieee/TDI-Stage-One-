import streamlit as st
from dashboard import run_dashboard
from prediction import run_prediction

# Set page config (must be first Streamlit command)
st.set_page_config(page_title="Loan Dashboard", page_icon="📊", layout="wide")

# Load and display logo and title
logo_path = "image\logo.png" 

# Header layout
col1, col2 = st.columns([1, 20])
with col1:
    st.image(logo_path, width=80)
with col2:
    st.markdown(
        """
        <h1 style='padding-top: 10px; padding-left: 0px; color: #c7522a; font-size: 50px;'>TDI Trust Bank</h1>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

# Navigation Sidebar
page = st.sidebar.radio("Navigation", ["Dashboard", "Predict Loan Approval"])

if page == "Dashboard":
    run_dashboard()
elif page == "Predict Loan Approval":
    run_prediction()
