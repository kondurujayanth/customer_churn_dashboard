import streamlit as st
import requests
import pandas as pd
import datetime

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title=" Customer Churn Prediction",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Custom CSS Styling
# ----------------------------
st.markdown("""
<style>
/* Main App Background */
.stApp {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    font-family: 'Arial', sans-serif;
    color: #333;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #a1c4fd, #c2e9fb, #89f7fe);
    padding: 20px;
    border-radius: 15px;
    color: #333;
}

/* Section Cards */
.section {
    background-color: white;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.1);
}

/* Prediction Button */
.stButton>button {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px 30px;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    transform: scale(1.05);
}

/* Table styling */
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

/* Prediction Card Animations */
@keyframes glowRed {
    0% { box-shadow: 0 0 15px rgba(255,0,0,0.4); }
    100% { box-shadow: 0 0 25px rgba(255,0,0,0.8); }
}
@keyframes glowGreen {
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

# ----------------------------
# Sidebar - About
# ----------------------------
st.sidebar.markdown("""
### ℹ️ About the App
This dashboard predicts the **Risk of customer churn** in a telecom company.

**Features Used:**
- InternetService_Fiber optic  
- PaymentMethod_Electronic check  
- PaperlessBilling  
- SeniorCitizen  
- StreamingTV_Yes  
- MonthlyCharges  

**Goal:** Identify high-risk customers for proactive retention.

**Model Type:** Binary Classification (Churn=1, No Churn=0)

Built with 
**FastAPI + Streamlit**  
Developer: 
**Konduru Jayanth**
""")

# ----------------------------
# Header
# ----------------------------
st.markdown('<div style="text-align:center"><h1>💼AI Powered Customer Churn Prediction🤖</h1></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:18px;">Enter customer details to predict churn risk</p>', unsafe_allow_html=True)

# ----------------------------
# Customer Input Section
# ----------------------------
with st.container():
    st.subheader("📋 Customer Information")
    st.caption("""
    ⚙️ **Input Details:**  
    - For all dropdowns, select **0 = No** and **1 = Yes**.  
    - Adjust the Monthly Charges as needed.
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
# Prediction Button
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
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #ff7f7f, #ff4b4b);
                    color:white;
                    padding:25px;
                    border-radius:20px;
                    text-align:center;
                    font-size:24px;
                    font-weight:bold;
                    box-shadow: 0 0 20px rgba(255,0,0,0.6);
                    animation: glowRed 1.5s infinite alternate;
                ">
                    🚨 <span style='font-size:30px; animation: pulse 1s infinite;'>High Risk!</span>  
                    Customer is likely to churn
                    <br><br>
                    <span style="font-size:16px;font-weight:normal; color:#fff8f0;">
                    💡 Retention Suggestions:<br>
                    - Offer loyalty discounts<br>
                    - Improve engagement & support<br>
                    - Provide value-added services
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #a0f7a0, #28a745);
                    color:white;
                    padding:25px;
                    border-radius:20px;
                    text-align:center;
                    font-size:24px;
                    font-weight:bold;
                    box-shadow: 0 0 20px rgba(0,200,0,0.6);
                    animation: glowGreen 1.5s infinite alternate;
                ">
                    💚 <span style='font-size:28px; animation: pulse 1s infinite;'>Low Risk!</span>  
                    Customer is not likely to churn
                    <br><br>
                    <span style="font-size:16px;font-weight:normal; color:#f0fff0;">
                    🎯 Retention Tips:<br>
                    - Maintain quality service<br>
                    - Offer loyalty rewards<br>
                    - Keep engagement high
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ No prediction received. Please try again.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}. Try again or check your internet connection.")

# ----------------------------
# Input Summary Table
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
    background: linear-gradient(135deg, #e0f7fa, #fce4ec, #fff3e0);
    padding: 12px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    color: #333333;
">
{df_input.to_html(index=False, escape=False)}
</div>
""", unsafe_allow_html=True)

# ----------------------------
# Prediction timestamp & Download
# ----------------------------
prediction_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(f"<p style='text-align:right; font-size:12px; color:gray;'>Last prediction: {prediction_time}</p>", unsafe_allow_html=True)

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














