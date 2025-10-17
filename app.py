import streamlit as st
import requests

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="💼 Customer Churn Prediction Dashboard",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# Custom Styling
# ---------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #e0f7fa, #fce4ec, #fff3e0);
    color: #333333;
}
.section {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}
.stButton>button {
    background: linear-gradient(90deg, #0072ff, #00c6ff);
    color: white;
    font-size: 18px;
    font-weight: bold;
    border-radius: 10px;
    padding: 10px 25px;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    transform: scale(1.03);
}
h1, h2, h3 {
    color: #004d7a;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar - About Section
# ---------------------------------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    st.markdown("## ℹ️ About the App")
    st.markdown("""
    This dashboard predicts whether a **telecom customer is likely to churn** based on their service usage and demographics.  

    **Features Used:**
    - `InternetService_Fiber optic`: Whether the customer uses fiber optic internet.  
    - `PaymentMethod_Electronic check`: If the payment method is electronic check.  
    - `PaperlessBilling`: Indicates if the customer uses paperless billing.  
    - `SeniorCitizen`: 1 if the customer is a senior citizen.  
    - `StreamingTV_Yes`: Whether the customer uses streaming TV.  
    - `MonthlyCharges`: Average monthly charges paid by the customer.  

    **Goal:**  
    Identify customers **at risk of churn** to help the company improve retention.

    **Model Type:**  
    Classification (Binary) – predicts `Churn (1)` or `No Churn (0)`.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# Main Page
# ---------------------------------------------------
st.title("💼 Customer Churn Prediction Dashboard")
st.write("Predict whether a customer is likely to **churn** or stay based on their service details.")

# ---------------------------------------------------
# Input Fields
# ---------------------------------------------------
with st.container():
    st.subheader("📋 Customer Information")
    col1, col2 = st.columns(2)

    with col1:
        internet_service = st.selectbox("Internet Service: Fiber Optic", [0, 1])
        payment_method = st.selectbox("Payment Method: Electronic Check", [0, 1])
        paperless_billing = st.selectbox("Paperless Billing", [0, 1])

    with col2:
        senior_citizen = st.selectbox("Senior Citizen", [0, 1])
        streaming_tv = st.selectbox("Streaming TV: Yes", [0, 1])
        monthly_charges = st.number_input(
            "Monthly Charges", 
            min_value=18.25, 
            max_value=118.75, 
            value=60.0, 
            step=0.5
        )

# ---------------------------------------------------
# Prediction Button
# ---------------------------------------------------
if st.button("🔍 Predict Churn"):
    data = {
        "features": [
            internet_service,
            payment_method,
            paperless_billing,
            senior_citizen,
            streaming_tv,
            monthly_charges
        ]
    }

    # Replace with your deployed FastAPI URL
    url = "https://customer-churn-api-pe3n.onrender.com/predict"

    try:
        response = requests.post(url, json=data)
        result = response.json()
        prediction = result.get("prediction", None)

        if prediction is not None:
            if prediction == 1:
                st.error("🚨 The customer is **likely to churn.**")
                st.info("""
                💡 **Suggestions to retain this customer:**
                - Offer loyalty discounts or exclusive packages.
                - Contact them via customer support to resolve possible issues.
                - Promote bundle services (like internet + streaming).
                """)
            else:
                st.success("✅ The customer is **not likely to churn.**")
                st.balloons()
                st.info("""
                🎯 **Retention Tips:**
                - Continue providing quality service.
                - Offer referral rewards to maintain engagement.
                - Keep satisfaction high with proactive communication.
                """)
        else:
            st.warning("⚠️ Unable to retrieve prediction from API. Please try again later.")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        st.warning("🌐 Please check your internet connection or try again later.")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("""
<hr>
<div style='text-align:center; font-size: 0.9rem; color: gray;'>
    🤖 Built with ❤️ using Streamlit & FastAPI
</div>
""", unsafe_allow_html=True)

