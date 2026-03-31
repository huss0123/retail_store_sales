
#import libraries
import streamlit as st 
import numpy as np
import pandas as pd 
import plotly.express as px 
import plotly.io as pio
pio.templates.default = "plotly"

#load data
df = pd.read_csv('clean_df.csv')

st.set_page_config(page_title="Retail Dashboard", layout="wide")

st.title("📊 Retail Transactions Dashboard")


st.set_page_config(layout="wide")


# --- Sidebar ---
with st.sidebar:

    page = st.radio(
        "📊 Retail Dashboard",
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

    st.subheader("📊 Key Performance Indicators")
    transactions_contribution = (filtered_df.shape[0] / df.shape[0]) * 100
    total_transactions = filtered_df.shape[0]
    total_revenue = filtered_df['Total Spent'].sum()
    avg_order_value = filtered_df['Total Spent'].mean()
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Transactions Contribution", f"{transactions_contribution:.2f}%")
    col2.metric("Total Transactions", f"{total_transactions:,}")
    col3.metric("Total Revenue", f"${total_revenue:,.2f}")
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

    st.markdown("---")

    top_customer = filtered_df.groupby('Customer ID')['Total Spent'].count().sort_values(ascending=False).reset_index().iloc[0]
    top_customer_name = top_customer['Customer ID']
    top_category = filtered_df.groupby('Category')['Total Spent'].sum().sort_values(ascending=False).reset_index().iloc[0]
    top_category_name = top_category['Category']
    top_item = filtered_df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).reset_index().iloc[0]
    top_item_name = top_item['Item']    
    col5, col6, col7 = st.columns(3)

    col5.metric("Top Customer", top_customer_name)
    col6.metric("Most Profitable Category", top_category_name)
    col7.metric("Best Selling Item", top_item_name)
    st.markdown("---")

    # Dataframe view
    st.dataframe(filtered_df)
    st.write(filtered_df.shape)

elif page == "📈 Exploratory Analysis":
    st.title("Exploratory Analysis")
    tab1, tab2, tab3 = st.tabs([
        "🔢 Numerical Analysis",
        "📊 Categorical Analysis",
        "⏱️ Time-Based Analysis"
        ])

    # =========================
    # 🔢 Numerical
    # =========================
    with tab1:
        st.markdown("## 🔢 Numerical Analysis")
        st.markdown("Explore distributions and relationships between numerical variables.")

        st.divider()

        st.markdown("### 📈 Distribution of Total Spent")
        fig11 = px.histogram(filtered_df, x="Total Spent", title="Distribution of Total Spent", marginal="box")
        st.plotly_chart(fig11)

        st.markdown("### 🔗 Relationship: Total Spent vs Quantity")
        fig12 = px.strip(filtered_df, x='Quantity', y='Total Spent')
        st.plotly_chart(fig12)


        st.markdown("### 🔗 Correlation Matrix")
        corr_matrix = filtered_df[['Price Per Unit', 'Total Spent', 'Quantity']].corr()
        fig13 = px.imshow(corr_matrix, text_auto=True, aspect="auto",color_continuous_scale='Blues')
        st.plotly_chart(fig13)

    # =========================
    # 📊 Categorical
    # =========================
    with tab2:
        st.markdown("## 📊 Categorical Analysis")
        st.markdown("Compare categories and understand revenue contribution.")

        st.divider()

        st.markdown("### 🏷️ Revenue by Category")
        top_cat = filtered_df.groupby(['Discount Applied', 'Category'])['Total Spent'].sum().sort_values(ascending=False).reset_index()
        fig21 = px.histogram(top_cat, x='Category', y='Total Spent', title='Total Spent by Category', color='Discount Applied')
        st.plotly_chart(fig21)

        col21, col22 = st.columns(2)
        with col21:
            st.markdown("### 📍 Location")
            fig22 = px.pie(filtered_df, names='Location', values='Total Spent')
            st.plotly_chart(fig22)
        with col22:
            st.markdown("### 💳 Payment Method")
            fig23 = px.pie(filtered_df, names='Payment Method', values='Total Spent')
            st.plotly_chart(fig23)

        st.markdown("### 🛒 Top Selling Item by Category")
        top_items = filtered_df.groupby(['Category', 'Item'])['Quantity'].sum().sort_values(ascending=False).reset_index()
        columns = ['Item', 'Quantity']
        top_items_cat = pd.DataFrame(columns=columns)

        for category in filtered_df['Category'].unique():
            cat_items = top_items[top_items['Category'] == category].sort_values(by='Quantity', ascending=False).head(1)
            top_items_cat = pd.concat([top_items_cat, cat_items], ignore_index=True)
        top_items_cat = top_items_cat.sort_values(by='Quantity', ascending=False)
        fig24 = px.bar(top_items_cat, x='Item', y='Quantity', title='Top Selling Item by Category', color='Category')
        st.plotly_chart(fig24)

    # =========================
    # ⏱️ Time-Based
    # =========================
    with tab3:
        filtered_df['day_of_week'] = filtered_df['Transaction Date'].dt.day_name()
        filtered_df['month_year'] = filtered_df['Transaction Date'].dt.to_period('M').astype(str)
        st.markdown("## ⏱️ Time-Based Analysis")
        st.markdown("Analyze trends, seasonality, and time patterns.")

        st.divider()

        st.markdown("### 📅 Revenue Over Time")
        revenue_time = filtered_df.groupby('Transaction Date')['Total Spent'].sum().reset_index()
        fig31= px.line(revenue_time, x='Transaction Date', y='Total Spent', title='Revenue Over Time')
        st.plotly_chart(fig31)

        st.markdown("### 📊 Monthly Trends")
        revenue_time = filtered_df.groupby('month_year')['Total Spent'].sum().reset_index()
        fig32 = px.line(revenue_time, x='month_year', y='Total Spent', title='Revenue Over Time')
        st.plotly_chart(fig32)

        st.markdown("### 📊 Day of Week Analysis")
        revenue_day = filtered_df.groupby('day_of_week')['Total Spent'].sum().reset_index()
        fig33 = px.bar(revenue_day, x='day_of_week', y='Total Spent', title='Revenue by Day of Week')
        st.plotly_chart(fig33)

elif page == "💡 Insights & Recommendations":
    st.title("Insights & Recommendations")


