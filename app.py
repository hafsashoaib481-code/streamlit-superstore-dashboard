import streamlit as st
import pandas as pd

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("Superstore Sales Dashboard")
st.write("Business Intelligence Assignment")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/superstore.csv")   # <-- now points to data folder
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region))
]

# ---------------- KPI METRICS ----------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", int(filtered_df["Sales"].sum()))
col2.metric("Total Profit", int(filtered_df["Profit"].sum()))
col3.metric("Total Orders", filtered_df["Order ID"].nunique())

# ---------------- SALES BY CATEGORY ----------------
st.subheader("Sales by Category")
category_sales = filtered_df.groupby("Category")["Sales"].sum()
st.bar_chart(category_sales)

# ---------------- SALES BY REGION ----------------
st.subheader("Sales by Region")
region_sales = filtered_df.groupby("Region")["Sales"].sum()
st.bar_chart(region_sales)

# ---------------- DATA PREVIEW ----------------
st.subheader("Filtered Data Preview")
st.dataframe(filtered_df.head(20))
