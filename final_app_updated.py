# final_app.py
import streamlit as st

<<<<<<< HEAD
=======

>>>>>>> 717cab16 (Commit changes)
# Set the page config at the start of final_app.py
st.set_page_config(page_title="Calmate and Dishify App", page_icon="🍽️")

# Sidebar Navigation
page = st.sidebar.selectbox("Select a page", ("Calmate", "Dishify"))

# Display selected page content
if page == "Calmate":
    from apps import CalMate as calMate
    calMate.main()
elif page == "Dishify":
    from apps import dishify as dishify
    dishify.main()
