import streamlit as st
import pandas as pd
from itertools import cycle

from src.app_utils.functions import get_book_id, add_book, add_rating, update_books


def show():

    col1, col2, col3 = st.columns(3)
    with col2:
        book_titles = st.session_state.df_books['title'].dropna().unique()
        option = st.selectbox("Add a book", [''] + book_titles)

    # Option Selectbox
    if option and get_book_id(st.session_state.df_books, option) not in st.session_state.df_user['ISBN'].tolist():
        st.session_state.df_user = add_book(
            st.session_state.df_user, 
            st.session_state['user_id'], 
            get_book_id(st.session_state.df_books, option)
        )

    # Show books
    cols = cycle(st.columns(6))
    df_user_book = pd.merge(st.session_state.df_user, st.session_state.df_books, on='ISBN', how='left')
    for index in range(len(df_user_book)):
        row = df_user_book.iloc[index]
        col = next(cols)
        # Image
        img_markdown = f"<img src='{row['image_url']}' width={200} height={300}></a><figcaption>{row['title']}</figcaption>"
        col.markdown(img_markdown, unsafe_allow_html=True)
        # Slider rating
        rating_key = f'rating_{index}'
        default_value = row['rating']
        rating= col.slider(f"Note", min_value=0.0, max_value=10.0, value=default_value, key=rating_key, step=0.5) 
        # Add or change the rating
        if rating != row['rating']:
            st.session_state.df_user=add_rating(st.session_state.df_user, row, rating)

    if st.button("Save books"):
        st.session_state.df_ratings = update_books(st.session_state.df_user, st.session_state.df_ratings, st.session_state['user_id'])
        st.session_state.saved = True
        # st.session_state.df_user.to_csv('user_books.csv', index=False)
        # st.session_state.df_ratings.to_csv('ratings_app.csv', index=False)
        st.success("Books saved!")

