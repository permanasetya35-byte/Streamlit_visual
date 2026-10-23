import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Customer Analytics Dashboard")

# Membaca file customers.csv (pake huruf 's')
try:
    df = pd.read_csv("customers.csv")
except FileNotFoundError:
    st.error("File 'customers.csv' tidak ditemukan!")
    st.stop()

st.sidebar.header("Filter Data")
departments = st.sidebar.multiselect("Pilih Department",
                                     df['Department'].dropna().unique())

genders = st.sidebar.multiselect("Pilih Gender",
                                 df['Gender'].dropna().unique())

st.sidebar.subheader("Filter Rentang Usia")
min_usia, max_usia = int(df['Age'].min()), int(df['Age'].max())
usia_range = st.sidebar.slider("Usia:", min_value=min_usia, max_value=max_usia,
                               value=(min_usia, max_usia))

# Filter data interaktif
df_filter = df[
    (df["Department"].isin(departments) if departments else True) & 
    (df["Gender"].isin(genders) if genders else True) &
    (df["Age"].between(usia_range[0], usia_range[1]))
]

st.subheader("Data Table")
st.dataframe(df_filter)

st.header("Visualisasi Statistik")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribusi Gender")
    pie_gender = px.pie(df_filter, names="Gender")
    st.plotly_chart(pie_gender)

with col2:
    st.subheader("Gaji rata-rata per Department")
    salary_by_dept = df_filter.groupby("Department")["AnnualSalary"].mean().reset_index()
    bar_salary = px.bar(salary_by_dept, x="Department", y="AnnualSalary")
    st.plotly_chart(bar_salary)