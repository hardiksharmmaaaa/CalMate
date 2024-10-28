# main_app.py
import streamlit as st
from updated_app import updated_app
from dishify import run_dishify_app
st.sidebar.title("Navigation")
app_selection = st.sidebar.selectbox("Choose an app", ["App 1", "App 2"])

if app_selection == "App 1":
    updated_app()
elif app_selection == "App 2":
    run_dishify_app()