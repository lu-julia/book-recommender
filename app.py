import streamlit as st
from streamlit_option_menu import option_menu

from pages import home, my_books
from src.app_utils.session import init_session_state



st.set_page_config(
        page_title="Your Next Read",
        page_icon="📚",
        layout="wide",
    )

st.markdown(
    """
    <h1 style='text-align: center; color: #2E4053; font-family: "Georgia", serif; font-size: 3em;'>
        Your Next Read 📚
    </h1>
    """,
    unsafe_allow_html=True
)

PAGES = {
    "Home": home,
    "My Books": my_books,
    #"Search": search
}


init_session_state()

selected = option_menu(
    menu_title=None, 
    options=["Home", "My Books", "Search"], 
    icons=['house', "book", "search"], 
    orientation="horizontal",
    menu_icon="cast", 
    default_index=0,
)

# Run selected page
page = PAGES[selected]
page.show()