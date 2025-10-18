import streamlit as st
import requests
import pandas as pd
import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="💼 Customer Churn Prediction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(120deg, #e0f7fa, #fce4ec, #fff3e0);
    color: #333333;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: #333333;
    font-family: 'Arial', sans-serif;
}

/* Section card */
.section {
    background-color: white;
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Smaller section for Input Summary */
.small-section {
    padding: 12px !important;
    margin-bottom: 12px !important;
    font-size: 14px !important;
}

/* Button style */
.stButton>button {
    background-color: #0072ff;
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 25px;
}
.stButton>button:hover {
    background-color: #00c6ff;
    color: white;
}

/* Input style */
.stNumberInput>div>div>input, .stSelectbox>div>div>select {
    border-radius: 8px;
    padding: 8px;
}

/* Compact Input Summary table */
.table-container table {
    border-collapse: collapse;
    width: 100%;
    font-size: 14px;
}
.table-container th, .table-container td {
    border: 1px solid #ddd;
    padding: 6px;
    text-align: center;
}
.table-container th {
    background-color: #f2f2f2;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Sidebar Info
# ----------------------------
st.sidebar.markdown("""
<div>
<p><b>About</b><br>This dashboard predicts the <b>risk of Customer Churn</b> in a telecom company using a trained ML model.</p>

<p><b>Features used:</b><br>
- InternetService_Fiber optic<br>
- PaymentMethod_Electronic check<br>
- PaperlessBilling<br>
- SeniorCitizen<br>
- StreamingTV_Yes<br>
- MonthlyCharges
</p>

<p>Built with 
<b>FastAPI + Streamlit</b></p>

<p>Developed by
<b>Konduru Jayanth</b></p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# App Header
# ----------------------------
st.markdown('<div style="text-align:center"><h1>💼 AI Powered Customer Churn Prediction 🤖</h1></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px;">Enter customer details to predict churn risk</p>', unsafe_allow_html=True)

# ----------------------------
# Input Section
# ----------------------------
with st.container():
    st.subheader("📋 Customer Information")
    st.caption("""
    ⚙️ **Input Details:**  
    - For dropdowns, select **0 = No** and **1 = Yes**.  
    - Adjust the Monthly Charges.
    """)
    col1, col2 = st.columns(2)

    with col1:
        internet_service = st.selectbox("Internet Service: Fiber Optic (0=No, 1=Yes)", [0,1])
        payment_method = st.selectbox("Payment Method: Electronic Check (0=No, 1=Yes)", [0,1])
        paperless_billing = st.selectbox("Paperless Billing (0=No, 1=Yes)", [0,1])

    with col2:
        senior_citizen = st.selectbox("Senior Citizen (0=No, 1=Yes)", [0,1])
        streaming_tv = st.selectbox("Streaming TV: (0=No, 1=Yes)", [0,1])
        monthly_charges = st.number_input("Monthly Charges ($)", min_value=18.25, max_value=118.75, value=60.0, step=0.5)

# ----------------------------
# Prediction Button with Spinner
# ----------------------------
if st.button("🔍 Predict Churn Risk"):

    url = "https://customer-churn-api-pe3n.onrender.com/predict"
    data = {"features": [internet_service, payment_method, paperless_billing, senior_citizen, streaming_tv, monthly_charges]}

    try:
        with st.spinner("Predicting churn risk..."):
            response = requests.post(url, json=data)
            response.raise_for_status()
            result = response.json()

        if "prediction" in result:
            pred = result["prediction"]

            if pred == 1:
                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #ff7f7f, #ff4b4b);
                        color:white;
                        padding:25px;
                        border-radius:20px;
                        text-align:center;
                        font-size:24px;
                        font-weight:bold;
                        box-shadow: 0 0 20px rgba(255,0,0,0.6);
                        animation: glow 1.5s infinite alternate;
                    ">
                        🚨 <span style='font-size:30px; animation: pulse 1s infinite;'>High Risk!</span>  
                        The customer might churn
                        <br><br>
                        <span style="font-size:16px;font-weight:normal; color:#fff8f0;">
                        💡 Suggestions to retain customer:<br>
                        - Offer loyalty discounts<br>
                        - Improve engagement & support<br>
                        - Provide value-added services
                        </span>
                    </div>
                    <style>
                    @keyframes glow {
                        0% { box-shadow: 0 0 15px rgba(255,0,0,0.4); }
                        100% { box-shadow: 0 0 25px rgba(255,0,0,0.8); }
                    }
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                    </style>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="
                        background: linear-gradient(135deg, #a0f7a0, #28a745);
                        color:white;
                        padding:25px;
                        border-radius:20px;
                        text-align:center;
                        font-size:24px;
                        font-weight:bold;
                        box-shadow: 0 0 20px rgba(0,200,0,0.6);
                        animation: glow 1.5s infinite alternate;
                    ">
                        💚 <span style='font-size:28px; animation: pulse 1s infinite;'>Low Risk!</span>  
                        The customer is not likely to churn
                        <br><br>
                        <span style="font-size:16px;font-weight:normal; color:#f0fff0;">
                        🎯 Retention Tips:<br>
                        - Maintain quality service<br>
                        - Offer loyalty rewards<br>
                        - Keep customer engagement high
                        </span>
                    </div>
                    <style>
                    @keyframes glow {
                        0% { box-shadow: 0 0 15px rgba(0,200,0,0.4); }
                        100% { box-shadow: 0 0 25px rgba(0,200,0,0.8); }
                    }
                    @keyframes pulse {
                        0% { transform: scale(1); }
                        50% { transform: scale(1.15); }
                        100% { transform: scale(1); }
                    }
                    </style>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No prediction received. Please try again.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}. Try again or check your internet connection.")

# ----------------------------
# Input Summary
# ----------------------------
st.subheader("📋 Input Summary")
input_data = {
    "InternetService_Fiber optic": [internet_service],
    "PaymentMethod_Electronic check": [payment_method],
    "PaperlessBilling": [paperless_billing],
    "SeniorCitizen": [senior_citizen],
    "StreamingTV_Yes": [streaming_tv],
    "MonthlyCharges": [monthly_charges]
}
df_input = pd.DataFrame(input_data)

st.markdown(f"""
<div class="table-container" style="
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: #333333;
    font-family: 'Arial', sans-serif;
    font-size: 14px;
">
{df_input.to_html(index=False, escape=False)}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Prediction timestamp & Download
# ----------------------------
prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"""
<p style="text-align:right; font-size:12px; color:gray;">
Last prediction timestamp: {prediction_time}
</p>
""", unsafe_allow_html=True)

st.download_button(
    label="📥 Download Input Summary as CSV",
    data=df_input.to_csv(index=False),
    file_name="customer_churn_input_summary.csv",
    mime="text/csv",
    help="Download the customer input data for your records"
)

# ----------------------------
# Footer
# ----------------------------
st.markdown("""
<hr>
<p style="text-align:center; font-size:14px;">
Made with ❤️ using <b>FastAPI + Streamlit</b> | Developed by <b>Konduru Jayanth</b>
</p>
""", unsafe_allow_html=True)
