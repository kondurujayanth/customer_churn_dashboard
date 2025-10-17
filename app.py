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
/* Main app background */
.stApp {
    background: linear-gradient(135deg, #e0f7fa, #fce4ec, #fff3e0);
    color: #333333;
}

/* Sidebar styling - toned down */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #a1c4fd, #c2e9fb);
    color: white;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
    color: white !important;
}

/* Section containers */
.section {
    background-color: white;
    border-radius: 18px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
}

/* Buttons */
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

/* Headings */
h1, h2, h3 {
    color: #004d7a;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Sidebar - About Section
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## ℹ️ About the App")
    st.markdown("""
    This dashboard predicts whether a **telecom customer is likely to churn** based on their service usage, billing type, and demographics.  

    ### 🔍 Features Used:
    - **InternetService_Fiber optic:** Whether the customer uses fiber optic internet.  
    - **PaymentMethod_Electronic check:** If the payment method is an electronic check.  
    - **PaperlessBilling:** Indicates whether the customer uses paperless billing.  
    - **SeniorCitizen:** 1 if the customer is a senior citizen, else 0.  
    - **StreamingTV_Yes:** Whether the customer uses streaming TV.  
    - **MonthlyCharges:** The average monthly bill paid by the customer.  

    ### 🎯 Goal:
    Identify **customers at risk of churn** to help the company take proactive retention steps.

    ### 🧠 Model Type:
    Binary Classification Model  
    (Predicts **Churn = 1** or **No Churn = 0**)
    """)

# ---------------------------------------------------
# Main Page
# ---------------------------------------------------
st.title("💼 Customer Churn Prediction Dashboard")
st.write("Predict whether a customer is likely to **churn** or stay based on their telecom service details.")

# ---------------------------------------------------
# Input Fields
# ---------------------------------------------------
with st.container():
    st.subheader("📋 Customer Information")
    st.caption("""
    ⚙️ **Input Details:**  
    - For all dropdowns, select **0 = No** and **1 = Yes**.  
    - Adjust the monthly charges to simulate customer billing scenarios.
    """)
    
    col1, col2 = st.columns(2)

    with col1:
        internet_service = st.selectbox("Internet Service: Fiber Optic (0 = No, 1 = Yes)", [0, 1])
        payment_method = st.selectbox("Payment Method: Electronic Check (0 = No, 1 = Yes)", [0, 1])
        paperless_billing = st.selectbox("Paperless Billing (0 = No, 1 = Yes)", [0, 1])

    with col2:
        senior_citizen = st.selectbox("Senior Citizen (0 = No, 1 = Yes)", [0, 1])
        streaming_tv = st.selectbox("Streaming TV: (0 = No, 1 = Yes)", [0, 1])
        monthly_charges = st.number_input(
            "Monthly Charges (in $)", 
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
                - Offer loyalty discounts or personalized bundles.
                - Improve customer engagement with dedicated support.
                - Provide value-added services or better contract offers.
                """)
            else:
                st.success("✅ The customer is **not likely to churn.**")
                st.balloons()
                st.info("""
                🎯 **Retention Tips:**
                - Maintain high service quality and reliability.
                - Offer small loyalty rewards to encourage long-term stay.
                - Keep consistent communication for engagement.
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
