import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px
import warnings
from streamlit_extras.metric_cards import style_metric_cards

def run_dashboard(): 
    warnings.filterwarnings('ignore')


    st.markdown('''
        <style>
        div.block-container {
            padding-top: 3rem;
            background: #004343;
        }
        .kpi-card {
            background: linear-gradient(to bottom right, #730220, #c7522a);
            padding: 1.5rem;
            margin: 0.8rem;
            border-radius: 1.2rem;
            box-shadow: 4px 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }
        .kpi-card:hover {
            transform: scale(1.03);
        }
        .plot-container {
            background-color: #c7522a;
            padding: 1.5rem;
            margin: 1rem 0.5rem;
            border-radius: 1rem;
            box-shadow: 0 6px 10px rgba(0,0,0,0.05);
        }
        </style>
    ''', unsafe_allow_html=True)

    st.title("Loan Approval Prediction & Insights Dashboard")

    df = pd.read_csv("Comprehensive_Banking_Database.csv")

    date_cols = ['Date Of Account Opening', 'Last Transaction Date', 'Transaction Date',
                 'Approval/Rejection Date', 'Payment Due Date', 'Last Credit Card Payment Date',
                 'Feedback Date', 'Resolution Date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if "reset" not in st.session_state:
        st.session_state.reset = False

    if st.button("Reset Filters"):
        st.session_state.reset = True
        st.rerun()

    st.sidebar.header("Filter Options")

    def multi_select_with_dropdown(label, options, default_all):
        expanded = st.sidebar.expander(label)
        with expanded:
            select_all = st.checkbox("Select All", value=True if st.session_state.reset else default_all, key=f"{label}_select_all")
            if select_all:
                selected = st.multiselect("Select", options, default=options, key=f"{label}_all_options")
            else:
                selected = st.multiselect("Select", options, key=f"{label}_options")
        return selected

    loan_status = multi_select_with_dropdown("Loan Status", df['Loan Status'].dropna().unique(), True)
    gender = multi_select_with_dropdown("Gender", df['Gender'].dropna().unique(), True)
    account_type = multi_select_with_dropdown("Account Type", df['Account Type'].dropna().unique(), True)
    city = multi_select_with_dropdown("City", df['City'].dropna().unique(), True)

    age_range = st.sidebar.slider("Age Range", int(df['Age'].min()), int(df['Age'].max()),
                                   (int(df['Age'].min()), int(df['Age'].max())) if st.session_state.reset else (int(df['Age'].min()), int(df['Age'].max())))

    loan_amt_range = st.sidebar.slider("Loan Amount Range", int(df['Loan Amount'].min()), int(df['Loan Amount'].max()),
                                       (int(df['Loan Amount'].min()), int(df['Loan Amount'].max())) if st.session_state.reset else (int(df['Loan Amount'].min()), int(df['Loan Amount'].max())))

    st.sidebar.markdown("---")
    st.sidebar.subheader("Filter by Date Ranges")
    date_filters = {}
    for col in date_cols:
        if col in df.columns:
            min_date = df[col].min()
            max_date = df[col].max()
            if pd.notnull(min_date) and pd.notnull(max_date):
                default_range = [min_date, max_date] if st.session_state.reset else [min_date, max_date]
                date_range = st.sidebar.date_input(f"{col} Range", default_range)
                if isinstance(date_range, list) and len(date_range) == 2:
                    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
                    date_filters[col] = (start, end)

    filtered_df = df[
        df['Loan Status'].isin(loan_status) &
        df['Gender'].isin(gender) &
        df['Account Type'].isin(account_type) &
        df['City'].isin(city) &
        df['Age'].between(age_range[0], age_range[1]) &
        df['Loan Amount'].between(loan_amt_range[0], loan_amt_range[1])
    ]

    for col, (start, end) in date_filters.items():
        filtered_df = filtered_df[filtered_df[col].between(pd.to_datetime(start), pd.to_datetime(end))]

    st.markdown("## KPI Summary")
    kpi_cols = st.columns(5)
    metrics = [
        ("\U0001F4C4 Total Applications", f"{len(filtered_df):,}"),
        ("\u2705 Approval Rate", f"{(len(filtered_df[filtered_df['Loan Status'] == 'Approved']) / len(filtered_df) * 100):.2f}%" if len(filtered_df) else "0.00%"),
        ("\u274C Rejection Rate", f"{(len(filtered_df[filtered_df['Loan Status'] == 'Rejected']) / len(filtered_df) * 100):.2f}%" if len(filtered_df) else "0.00%"),
        ("\U0001F4B0 Avg Loan Amount", f"${filtered_df['Loan Amount'].mean():,.2f}"),
        ("\U0001F4C8 Avg Interest Rate", f"{filtered_df['Interest Rate'].mean():.2f}%")
    ]
    for col, (label, val) in zip(kpi_cols, metrics):
        col.markdown(f"<div class='kpi-card'><h5>{label}</h5><h3>{val}</h3></div>", unsafe_allow_html=True)

    style_metric_cards()

    st.markdown("## Visual Insights")
    vcol1, vcol2 = st.columns(2)

    with vcol1:
        with st.container():
            st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
            st.subheader("Loan Status Distribution")
            fig1 = px.pie(filtered_df, names='Loan Status', title="Loan Status Share", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
            st.plotly_chart(fig1, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
            st.subheader("Loan Amount by Status")
            fig3 = px.box(filtered_df, x="Loan Status", y="Loan Amount", color="Loan Status", title="Loan Amount Distribution", color_discrete_sequence=px.colors.qualitative.Prism)
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with vcol2:
        with st.container():
            st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
            st.subheader("Age Distribution")
            fig2 = px.histogram(filtered_df, x="Age", nbins=30, title="Age Histogram", color_discrete_sequence=['#1f77b4'])
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with st.container():
            st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
            st.subheader("Interest Rate by Loan Type")
            fig4 = px.violin(filtered_df, y="Interest Rate", x="Loan Type", color="Loan Type", box=True, points="all", color_discrete_sequence=px.colors.sequential.Aggrnyl)
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    if 'Approval/Rejection Date' in filtered_df.columns:
        st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
        st.subheader("Loan Application Trends Over Time")
        filtered_df["Month"] = filtered_df['Approval/Rejection Date'].dt.to_period("M").astype(str)
        time_series = filtered_df.groupby("Month")["Loan Amount"].sum().reset_index()
        fig5 = px.line(time_series, x="Month", y="Loan Amount", title="Monthly Loan Volume", markers=True, line_shape="spline", color_discrete_sequence=['#636EFA'])
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
    st.subheader("Correlation Matrix")
    numeric_cols = ['Age', 'Account Balance', 'Transaction Amount', 'Loan Amount', 'Interest Rate', 'Loan Term', 'Credit Limit', 'Credit Card Balance', 'Minimum Payment Due', 'Rewards Points']
    corr_matrix = filtered_df[numeric_cols].corr()
    fig6 = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r", title="Correlation Heatmap")
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='plot-container'>", unsafe_allow_html=True)
    st.subheader("Download Filtered Dataset")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="filtered_loan_data.csv", mime="text/csv")
    st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.reset = False

if __name__ == "__main__":
    run_dashboard()
