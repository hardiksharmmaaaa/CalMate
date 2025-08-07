import streamlit as st 

# --- Page Setup ---

CalMate_page=st.Page(
    page="projects/calMate.py",
    title="Calmate",
    icon="🍽️",
    default=True
)

Dishify_page=st.Page(
    page="projects/dishify.py",
    title="Dishify",
    icon="👨‍🍳"
)


# --- Navigation Setup --- 

pg=st.navigation(pages=[CalMate_page,Dishify_page])

# --- Run Navigation --- 

pg.run()