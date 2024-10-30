# final_app.py
import streamlit as st

# Set the page config at the start of final_app.py
st.set_page_config(page_title="Calmate and Dishify App", page_icon="🍽️")

# Sidebar Navigation
page = st.sidebar.selectbox("Select a page", ("Calmate", "Dishify"))

# Display selected page content
if page == "Calmate":
    from projects import CalMate as calMate
    calMate.main()
elif page == "Dishify":
    from projects import dishify as dishify
    dishify.main()
