import streamlit as st
import pandas as pd
from utils.db import connect_db

# Function Monitor Data
def view_reports_page():

    st.title("รายงานจากอาสาสมัคร")
    conn = connect_db()
    if conn:
        df = pd.read_sql("SELECT * FROM reports", conn)

        df.set_index('id', inplace=True)
        conn.close()
        st.dataframe(df.style.hide(axis="index"))

    else:
        st.error("Can't connect to Database.")