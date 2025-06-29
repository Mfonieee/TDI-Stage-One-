import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from dashboard import run_dashboard
from prediction import run_prediction

st.set_page_config(page_title="Loan Dashboard", page_icon="📊", layout="wide")

# Navigation
page = st.sidebar.radio("Navigation", ["Dashboard", "Predict Loan Approval"])

if page == "Dashboard":
    run_dashboard()
elif page == "Predict Loan Approval":
    run_prediction()
