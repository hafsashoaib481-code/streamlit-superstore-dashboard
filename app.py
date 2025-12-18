import streamlit as st
import pandas as pd
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Superstore BI Dashboard", layout="wide")

st.title("📊 Superstore Sales Dashboard")
st.caption("Business Intelligence Assignment – Interactive Analysis")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    file_path = os.path.join("data", "superstore.csv")

    if not os.path.exists(file_path):
        st.error("❌ superstore.csv not found in data folder")
        st.stop()

    df = pd.read_csv(file_path)

    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Year"] = df["Order Date"].dt.year

    # Remove rows with missing essential values
    df = df.dropna(subset=["Category", "Region", "Sales", "Profit", "Year"])

    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

year = st.sidebar.multiselect(
    "Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Year"].isin(year))
]

# ---------- KPI SECTION ----------
st.markdown("## 📌 Key Performance Indicators")

k1, k2, k3 = st.columns(3)

k1.metric("💰 Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
k2.metric("📈 Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
k3.metric("🧾 Total Orders", filtered_df["Order ID"].nunique())

st.markdown("---")

# ---------- TABS FOR VISUALS ----------
tab1, tab2, tab3 = st.tabs(["📊 Sales Analysis", "📈 Profit Analysis", "📋 Data View"])

# ===== TAB 1 =====
with tab1:
    left, right = st.columns(2)

    with left:
        st.subheader("Sales by Category")
        st.bar_chart(filtered_df.groupby("Category")["Sales"].sum())

    with right:
        st.subheader("Sales by Region")
        st.bar_chart(filtered_df.groupby("Region")["Sales"].sum())

    if "Sub-Category" in filtered_df.columns:
        st.subheader("Sales by Sub-Category")
        st.bar_chart(filtered_df.groupby("Sub-Category")["Sales"].sum())

# ===== TAB 2 =====
with tab2:
    st.subheader("Profit vs Sales")
    st.scatter_chart(filtered_df, x="Sales", y="Profit")

    st.subheader("Year-wise Sales Trend")
    st.line_chart(filtered_df.groupby("Year")["Sales"].sum())

# ===== TAB 3 =====
with tab3:
    st.subheader("Filtered Dataset Preview")
    st.dataframe(filtered_df.head(50))
