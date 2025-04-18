"""
Page to add books to the user's collection and rate them.
"""

from itertools import cycle

import streamlit as st
import pandas as pd

from src.app_utils.logger import logger
from src.app_utils.functions import get_book_id, add_book, add_rating, update_books
from src.app_utils.ui_elements import render_my_books_instructions


def show():

    if len(st.session_state.df_user) == 0 or not st.session_state.saved:
        render_my_books_instructions()
    else:
        st.info(
            """✅ You've already added some books! Feel free to rate more or update your ratings.
            Save your changes when you're done."""
        )

    _, col2, _ = st.columns(3)
    with col2:
        # Create label for books: "Title - Author"
        st.session_state.df_books["label"] = (
            st.session_state.df_books["title"].fillna("")
            + " - "
            + st.session_state.df_books["author"].fillna("")
        )
        book_labels = st.session_state.df_books["label"].dropna().unique()

        option = st.selectbox(
            label="Add a book",
            options=book_labels,
            index=None,
            placeholder="Search a book by title or author",
        )

    # Add selected book if not already added
    if option:
        # Extract title from label
        selected_title = option.split(" - ")[0]
        isbn = get_book_id(st.session_state.df_books, selected_title)
        user_id = st.session_state["user_id"]
        if isbn not in st.session_state.df_user["ISBN"].tolist():
            st.session_state.df_user = add_book(st.session_state.df_user, user_id, isbn)
            logger.info(f"Book {isbn} added to user {user_id}'s collection.")

    # Show books
    cols = cycle(st.columns(6))
    df_user_book = pd.merge(
        st.session_state.df_user, st.session_state.df_books, on="ISBN", how="left"
    )

    for index, row in df_user_book.iterrows():
        col = next(cols)
        with col:
            # Book cover and title
            st.markdown(
                f"""
                <img src='{row['image_url']}' width=200 height=290><br><b>{row["title"]}</b>
                """,
                unsafe_allow_html=True,
            )
            # Rating slider
            rating_key = f"rating_{index}"
            default_value = row["rating"]
            rating = st.slider(
                "Note",
                min_value=0.0,
                max_value=10.0,
                value=default_value,
                key=rating_key,
                step=0.5,
            )
            # Update rating if changed
            if rating != row["rating"]:
                st.session_state.df_user = add_rating(
                    st.session_state.df_user, row, rating
                )
                logger.info(
                    f"Rating for book {row['ISBN']} updated to {rating} for user {row['user_id']}."
                )

    if st.button("💾 Save books"):
        st.session_state.df_ratings = update_books(
            df_user=st.session_state.df_user,
            df_ratings=st.session_state.df_ratings,
            user_id=st.session_state["user_id"],
        )
        st.session_state.saved = True
        st.success(
            "✅ Books saved! You can now go to the Home page to see your recommendations."
        )
        st.session_state["ratings_updated"] = True
        logger.info(
            f"User {st.session_state['user_id']} saved their books and ratings."
            f" {len(st.session_state.df_user)} books in the user's collection."
        )
