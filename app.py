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

init_session_state()


st.markdown(
    """
    <h1 style='text-align: center; color: #2E4053; font-family: "Georgia", serif; font-size: 3em;'>
        Your Next Read 📚
    </h1>
    """,
    unsafe_allow_html=True,
)


# Default menu page
if st.session_state.current_page == "search":
    DEFAULT = 2
else:
    DEFAULT = 0


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
