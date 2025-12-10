import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Product Return Prediction", layout="centered")
st.title("Product Return Prediction App")

# Load the trained model
model = joblib.load("final_model.joblib")

# --- User Inputs ---
st.header("Order Information")

Product = st.selectbox("Product", ["Smartphone", "Monitor", "Laptop", "Headphones", "Smartwatch", "Tablet"])
Category = st.selectbox("Category", ["Phones", "Accessories", "Computers", "Wearables", "Tablets"])
Price = st.number_input("Price", min_value=0.0, value=50000.0)
Quantity = st.number_input("Quantity", min_value=1, value=1)
PaymentMethod = st.selectbox("Payment Method", ["Credit Card", "PayPal", "Cash", "Wire Transfer"])
DeliveryDays = st.number_input("Delivery Days", min_value=0, value=15)
SatisfactionRating = st.number_input("Satisfaction Rating (1-5)", min_value=1, max_value=5, value=3)
Municipality = st.selectbox("Municipality", ["Cocody", "Abobo", "Bingerville", "Marcory"])

# --- Mapping (same as during training) ---
product_map = {'Smartphone':1,'Monitor':2,'Laptop':3,'Headphones':4,'Smartwatch':5,'Tablet':6}
category_map = {'Phones':1,'Accessories':2,'Computers':3,'Wearables':4,'Tablets':5}
payment_map = {'Credit Card':1,'PayPal':2,'Cash':3,'Wire Transfer':4}
municipality_map = {'Cocody':1,'Abobo':2,'Bingerville':3,'Marcory':4}

# --- Build the DataFrame with the correct structure ---
input_df = pd.DataFrame({
    "Product": [product_map[Product]],
    "Category": [category_map[Category]],
    "Price": [float(Price)],
    "Quantity": [int(Quantity)],
    "PaymentMethod": [payment_map[PaymentMethod]],
    "DeliveryDays": [int(DeliveryDays)],
    "SatisfactionRating": [int(SatisfactionRating)],
    "Municipality": [municipality_map[Municipality]]
})

# Ensure column order matches the model
try:
    input_df = input_df[model.feature_names_in_]
except:
    st.error("❌ Error: The input columns do not match the model's expected features.")
    st.write("Expected columns:", model.feature_names_in_)
    st.write("Provided columns:", input_df.columns.tolist())
    st.stop()

# --- Prediction ---
if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0][1]

    st.subheader("Prediction Result")
    st.write(f"Probability that the product will be returned: **{prediction_proba*100:.2f}%**")

    if prediction == 1:
        st.error("⚠️ The product is likely to be returned.")
    else:
        st.success("✅ The product is unlikely to be returned.")
