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

# Logo au centre
"""
col1, col2, col3 = st.columns(3) 
with col2:
    st.image("images/logo.png", width=300)"""


st.markdown(
    """
    <div style="text-align: center;">
        <img src="images/logo.png" style="width:300px;" />
    </div>
    """,
    unsafe_allow_html=True
)



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
