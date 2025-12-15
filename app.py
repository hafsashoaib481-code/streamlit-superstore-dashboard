import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Superstore Dashboard", layout="wide")
st.title("Superstore Sales Dashboard")
st.write("Business Intelligence Assignment")

@st.cache_data
def load_data():
    file_path = os.path.join("data", "superstore.csv")

    if not os.path.exists(file_path):
        st.error("❌ superstore.csv not found in data folder")
        st.stop()

    df = pd.read_csv(file_path)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

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

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Total Orders", filtered_df["Order ID"].nunique())

st.subheader("Sales by Category")
st.bar_chart(filtered_df.groupby("Category")["Sales"].sum())

st.subheader("Sales by Region")
st.bar_chart(filtered_df.groupby("Region")["Sales"].sum())

st.subheader("Data Preview")
st.dataframe(filtered_df.head(20))
