import streamlit as st
import pandas as pd
import plotly.express as px

# ================================
# Page config
# ================================
st.set_page_config(page_title="Interactive Product Return Dashboard", layout="wide")
st.title("📊 Interactive Product Return Analysis Dashboard")

# ================================
# Data
# ================================
DATA_FILE = "DataSales.csv"

try:
    data = pd.read_csv(DATA_FILE)
    st.success(f"{DATA_FILE} loaded successfully!")
except FileNotFoundError:
    st.error(f"❌ The file {DATA_FILE} was not found.")
    st.stop()

# ================================
# Sidebar filters
# ================================
st.sidebar.header("Filters")

if "Category" in data.columns:
    selected_category = st.sidebar.multiselect(
        "Filter by Category",
        options=data["Category"].unique(),
        default=data["Category"].unique()
    )
    data = data[data["Category"].isin(selected_category)]

# ================================
# Interactive layout configuration
# ================================
def interactive_layout(fig):
    fig.update_layout(
        hovermode="x unified",
        dragmode="zoom",
        template="plotly_white",
    )
    return fig

# ================================
# 1️⃣ Return Rate (Pie)
# ================================
st.header("1️⃣ Overall Return Rate")

return_rate = data["Returned"].mean()

fig_pie = px.pie(
    names=["Returned", "Not Returned"],
    values=[return_rate, 1-return_rate],
    title="Overall Return Rate",
    hole=0.4
)
fig_pie = interactive_layout(fig_pie)
st.plotly_chart(fig_pie, use_container_width=True)

# ================================
# 2️⃣ Most Returned Products
# ================================
st.header("2️⃣ Most Returned Products")

top_products = (
    data.groupby("Product")["Returned"].sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_prod = px.bar(
    top_products,
    x="Returned",
    y="Product",
    orientation="h",
    title="Most Returned Products",
)
fig_prod = interactive_layout(fig_prod)

# Dropdown for sorting
fig_prod.update_layout(
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            x=1.2,
            y=1.15,
            buttons=[
                dict(label="Sort Descending", method="update",
                     args=[{"x": [top_products.sort_values(by="Returned", ascending=False)["Returned"]],
                           "y": [top_products.sort_values(by="Returned", ascending=False)["Product"]]}]),
                dict(label="Sort Ascending", method="update
