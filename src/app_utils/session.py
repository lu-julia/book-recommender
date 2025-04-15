"""
This module initializes the session state variables used in the app.
"""

import streamlit as st

from src.data.load_data import load_rating_data, load_books_ratings
from src.app_utils.functions import get_my_books


def init_session_state() -> None:
    """
    Initialize the session state variables used in the app.
    """
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = -1
    if "df_books" not in st.session_state and "df_user" not in st.session_state:
        st.session_state.df_books = load_books_ratings()
        st.session_state.df_ratings = load_rating_data()
        st.session_state.df_user = get_my_books(
            st.session_state.df_ratings, st.session_state["user_id"]
        )
    if "saved" not in st.session_state:
        st.session_state.saved = False
    if "selected_book" not in st.session_state:
        st.session_state.selected_book = None
    if "previous_page" not in st.session_state:
        st.session_state.previous_page = "home"
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"

    # --- Session defaults for filters ---
    if "search_query" not in st.session_state:
        st.session_state.search_query = ""
    if "year_from" not in st.session_state:
        st.session_state.year_from = int(st.session_state.df_books["year"].min())
    if "year_to" not in st.session_state:
        st.session_state.year_to = int(st.session_state.df_books["year"].max())
    if "sort_by" not in st.session_state:
        st.session_state.sort_by = "None"
    if "page" not in st.session_state:
        st.session_state.page = 0
    if "filters_cleared" not in st.session_state:
        st.session_state.filters_cleared = False
