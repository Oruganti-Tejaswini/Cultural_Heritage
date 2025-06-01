import streamlit as st
import base64

# Function to inject logo
def add_logo(logo_path, size=80):
    with open(logo_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
        .fixed-header-logo {{
            position: fixed;
            top: 15px;
            left: 15px;
            z-index: 999999;
            width: {size}px;
            height: auto;
            border-radius: 20%;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
            transition: transform 0.3s ease;
        }}
        .fixed-header-logo:hover {{
            transform: scale(1.1);
        }}
        </style>
        <img class="fixed-header-logo" src="data:image/png;base64,{encoded}">
    """, unsafe_allow_html=True)
