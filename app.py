
#import libraries
import streamlit as st 
import numpy as np
import pandas as pd 
import plotly.express as px 


#load data
df = pd.read_csv('clean_df.csv')

st.set_page_config(page_title="Retail Dashboard", layout="wide")

st.title("📊 Retail Transactions Dashboard")


st.set_page_config(layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #0E1117;
}

/* Title styling */
.sidebar-title {
    font-size: 22px;
    font-weight: bold;
    color: #00C6FF;
    margin-bottom: 10px;
}

/* Radio buttons spacing */
div[role="radiogroup"] > label {
    padding: 5px;
    margin: 5px 0;
    border-radius: 8px;
}

/* Hover effect */
div[role="radiogroup"] > label:hover {
    background-color: #262730;
    cursor: pointer;
}

/* Selected option */
div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {
    background-color: #00C6FF !important;
}

/* Text styling */
div[role="radiogroup"] label span {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Retail Dashboard</div>', unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Overview", "📈 Exploratory Analysis", "💡 Insights & Recommendations"]
    )

    st.markdown("---")


# -------------------------------
# ensure datetime format
# -------------------------------
df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
filtered_df = df.copy()


# -------------------------------
# Sidebar UI
# -------------------------------
st.sidebar.markdown("## 🔍 Filters")
st.sidebar.markdown("---")

# 1. Date filter    
min_date = df["Transaction Date"].min()
max_date = df["Transaction Date"].max()

date_range = st.sidebar.date_input(
        "📅 Transaction Date",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
#Apply Date filter
if len(date_range) == 2:
    start, end = pd.to_datetime(date_range)
    filtered_df = filtered_df[
        (filtered_df["Transaction Date"] >= start) &
        (filtered_df["Transaction Date"] <= end)
    ]

# 2. Category filter
category_options = df["Category"].unique()
category = st.sidebar.multiselect("📂 Category", category_options)
# Apply Category filter
if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# 3. Item filter (depends on category)

item_options = df[df["Category"].isin(category)]["Item"].unique()
item = st.sidebar.multiselect("🛒 Item", item_options)
# Apply Item filter
if item:
    filtered_df = filtered_df[filtered_df["Item"].isin(item)]

# 4. Payment Method filter
payment_options = df["Payment Method"].unique() 
payment = st.sidebar.multiselect("💳 Payment Method", payment_options)
# Apply Payment filter
if payment:
    filtered_df = filtered_df[filtered_df["Payment Method"].isin(payment)]

# 5. Location filter
location_options = df["Location"].unique()
location = st.sidebar.multiselect("📍 Location", location_options)
# Apply Location filter
if location:
    filtered_df = filtered_df[filtered_df["Location"].isin(location)]


st.sidebar.markdown("---")

st.sidebar.caption("Built by Hussein Ahmed | Epsilon AI Academy")








# --- Routing ---
if page == "🏠 Overview":
    st.title("Overview")
    st.dataframe(filtered_df)
    st.write(filtered_df.shape)

elif page == "📈 Exploratory Analysis":
    st.title("Exploratory Analysis")

elif page == "💡 Insights & Recommendations":
    st.title("Insights & Recommendations")


