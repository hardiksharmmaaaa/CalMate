import streamlit as st

# Sidebar Navigation
page = st.sidebar.selectbox("Select a page", ("Calmate", "Dishify"))

# Display selected page content
if page == "Calmate":
    import projects.calMate as calMate  # Adjust path if necessary
    calMate.main()  # Assuming main() is the function to display content in calMate.py
elif page == "Dishify":
    import projects.dishify as dishify
    dishify.main()  # Assuming main() is the function to display content in dishify.py
