"""
Page to add books to the user's collection and rate them.
"""

import streamlit as st
import pandas as pd
from itertools import cycle

from src.app_utils.functions import (
    get_book_id,
    add_book,
    add_rating,
    update_books
)


def show():
    col1, col2, col3 = st.columns(3)
    with col2:
        # Create label for books: "Title - Author"
        st.session_state.df_books['label'] = st.session_state.df_books['title'].fillna('') + " - " + st.session_state.df_books['author'].fillna('')
        book_labels = st.session_state.df_books['label'].dropna().unique()

        option = st.selectbox(
            label="Add a book", 
            options=book_labels, 
            index=None, 
            placeholder="Search a book by title or author"
        )

    # Add selected book if not already added
    if option:
        # Extract title from label
        selected_title = option.split(" - ")[0]
        isbn = get_book_id(st.session_state.df_books, selected_title)
        if isbn not in st.session_state.df_user['ISBN'].tolist():
            st.session_state.df_user = add_book(
                st.session_state.df_user, 
                st.session_state['user_id'], 
                isbn
            )

    # Show books
    cols = cycle(st.columns(6))
    df_user_book = pd.merge(st.session_state.df_user, st.session_state.df_books, on='ISBN', how='left')

    for index in range(len(df_user_book)):
        row = df_user_book.iloc[index]
        col = next(cols)
        with col:
            # Book cover and title
            st.markdown(f"<img src='{row['image_url']}' width=200 height=300><br><b>{row['title']}</b>", unsafe_allow_html=True)
            # Rating slider
            rating_key = f'rating_{index}'
            default_value = row['rating']
            rating = st.slider("Note", min_value=0.0, max_value=10.0, value=default_value, key=rating_key, step=0.5)
            # Update rating if changed
            if rating != row['rating']:
                st.session_state.df_user = add_rating(st.session_state.df_user, row, rating)


    if st.button("💾 Save books"):
        st.session_state.df_ratings = update_books(
            df_user=st.session_state.df_user, 
            df_ratings=st.session_state.df_ratings, 
            user_id=st.session_state['user_id']
        )
        st.session_state.saved = True
        st.success("Books saved!")
