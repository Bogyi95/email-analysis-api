import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("emails.db")
df = pd.read_sql_query("SELECT * FROM emails", conn)
st.title("Email Analysis Dashboard")
st.write("Total emails analyzed:", len(df))
st.subheader("Email categories")
st.bar_chart(df["category"].value_counts())
st.subheader("Priority distribution")
st.bar_chart(df["priority"].value_counts())
st.dataframe(df)
