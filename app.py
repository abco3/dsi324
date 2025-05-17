import streamlit as st
from modules.main_app import main

#st.set_page_config(layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit&display=swap');
        
        html, body, div, p, label, input, textarea, button, h1, h2, h3, h4, h5, h6, span {
            font-family: 'Kanit', sans-serif !important;
        }
    </style>
""", unsafe_allow_html=True)


if __name__ == "__main__":
    main()