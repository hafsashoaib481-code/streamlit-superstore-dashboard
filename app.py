import streamlit as st
import pandas as pd
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Superstore BI Dashboard",
    layout="wide"
)

# ---------- TITLE ----------
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
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()
    return df

df = load_data()

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Select Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

year = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Region"].isin(region)) &
    (df["Year"].isin(year))
]

st
