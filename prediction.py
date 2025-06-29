import streamlit as st
import pandas as pd
import numpy as np
import pickle

def run_prediction():
    # The trained LightGBM pipeline model
    with open("lightgbm_model.pkl", "rb") as file:
        model = pickle.load(file)

    # Title and description
    st.title("Loan Approval Prediction")
    st.markdown("Enter customer details to predict whether their loan will be approved.")

    #  User Input Form 
    with st.form("prediction_form"):
        st.subheader("Customer & Loan Information")

        account_balance = st.number_input("Account Balance ($)", min_value=0.0, format="%.2f", step=100.0)

        age = st.slider("Age", min_value=18, max_value=100, value=30, step=1)

        account_type = st.selectbox("Account Type", options=["Savings", "Current"])

        loan_amount = st.number_input("Loan Amount Requested ($)", min_value=0.0, format="%.2f", step=500.0)

        interest_rate = st.slider("Interest Rate (%)", min_value=0.0, max_value=100.0, value=10.0, step=0.5)

        transaction_amount = st.number_input("Last Transaction Amount ($)", min_value=0.0, format="%.2f", step=100.0)

        loan_term = st.selectbox("Loan Term (in months)", options=[6, 12, 18, 24, 36, 48, 60])

        submitted = st.form_submit_button("Predict Loan Status")

    # Prediction Logic 
    if submitted:
        try:
            # Create input DataFrame
            input_data = pd.DataFrame([{
                'Account Balance': account_balance,
                'Age': age,
                'Account Type': account_type,
                'Loan Amount': loan_amount,
                'Interest Rate': interest_rate,
                'Transaction Amount': transaction_amount,
                'Loan Term': loan_term
            }])

            # Make prediction
            prediction = model.predict(input_data)[0]
            probability = model.predict_proba(input_data)[0][1]

            # Display result
            st.markdown("### 🎯Prediction Result")
            if prediction == 1:
                st.success(f"✅ Loan is **likely to be approved** (Confidence: {probability:.2%})")
            else:
                st.error(f"❌ Loan is **likely to be rejected** (Confidence: {1 - probability:.2%})")

        except Exception as e:
            st.error(f"⚠️ An error occurred during prediction: {e}")
