import streamlit as st
import requests
import plotly.graph_objects as go

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="💼 Customer Churn Prediction Dashboard",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# Custom Styling
# ---------------------------------------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        }
        h1 {
            color: #004d7a;
            text-align: center;
            font-size: 2.3rem;
        }
        .stButton>button {
            background-color: #004d7a;
            color: white;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0074b7;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Title
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
        monthly_charges = st.number_input("Monthly Charges", min_value=18.25, max_value=118.75, value=60.0, step=0.5)

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
                st.info("💡 **Suggestion:** Offer discounts, improve service experience, and provide retention incentives.")
            else:
                st.success("✅ The customer is **not likely to churn.**")
                st.balloons()
                st.info("🎯 **Keep it up!** Continue delivering excellent service to maintain loyalty.")

            # ---------------------------------------------------
            # Visualizations
            # ---------------------------------------------------
            st.subheader("📊 Risk Factor Visualization")

            fig = go.Figure(data=[
                go.Bar(
                    x=["InternetService", "PaymentMethod", "PaperlessBilling", "SeniorCitizen", "StreamingTV"],
                    y=[internet_service, payment_method, paperless_billing, senior_citizen, streaming_tv],
                    marker_color=['#004d7a', '#0074b7', '#00a8e8', '#0074b7', '#004d7a']
                )
            ])
            fig.update_layout(
                title="Customer Risk Factors",
                xaxis_title="Features",
                yaxis_title="Binary Value (0 or 1)",
                plot_bgcolor='white',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

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
