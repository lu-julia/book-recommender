"""
Main app file for the book recommendation app.
"""

import streamlit as st
from streamlit_option_menu import option_menu

from pages import home, my_books, search
from src.app_utils.session import init_session_state


st.set_page_config(
    page_title="Your Next Read",
    page_icon="📚",
    layout="wide",
)

with st.spinner("Loading... This may take a few seconds."):
    init_session_state()

# Reduce whitespace on the top of the page
st.markdown(
    """
<style>
.block-container
{
    padding-top: 1.5rem;
    padding-bottom: 5rem;
    margin-top: 1rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# Logo
_, col2, _ = st.columns(3)
with col2:
    st.image("images/logo.png", width=300, use_container_width=True)

# Add space between logo and menu
st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

# Default menu page
DEFAULT = 2 if st.session_state.current_page == "search" else 0

selected = option_menu(
    menu_title=None,
    options=["Home", "My Books", "Search"],
    icons=["house", "book", "search"],
    orientation="horizontal",
    menu_icon="cast",
    default_index=DEFAULT,
)

# Run selected page
PAGES = {
    "Home": home,
    "My Books": my_books,
    "Search": search,
}
page = PAGES[selected]
page.show()
