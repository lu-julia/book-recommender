"""
Utility functions for the book recommendation app.
"""

from itertools import cycle
import streamlit as st
import pandas as pd


def get_my_books(df_ratings: pd.DataFrame, user_id: int) -> pd.DataFrame:
    """
    Get the books rated by a specific user.
    """
    result = df_ratings.loc[df_ratings["user_id"] == user_id]
    return result


def get_book_id(df_books: pd.DataFrame, title: str) -> str:
    """
    Get the ISBN of a book by its title.
    """
    result = df_books.loc[df_books['title'] == title, 'ISBN']
    return result.iloc[0]


def add_book(df_user: pd.DataFrame, user_id: int, isbn: str) -> pd.DataFrame:
    """
    Add a new book to the user's collection.
    """
    new_row = {
        'user_id': user_id,
        'ISBN': isbn,
        'rating': 0.0
    }
    df_new_row = pd.DataFrame([new_row])
    df_user = pd.concat([df_user, df_new_row], ignore_index=True)
    return df_user


def add_rating(df_user: pd.DataFrame, row: pd.Series, rating: float) -> pd.DataFrame:
    """
    Update the rating of a book in the user's collection.
    """
    df_user.loc[
        (df_user['ISBN'] == row['ISBN']) &
        (df_user['user_id'] == row['user_id']), 'rating'
    ] = rating
    return df_user


def update_books(df_user: pd.DataFrame, df_ratings: pd.DataFrame, user_id: int) -> pd.DataFrame:
    """
    Add the user's ratings to the ratings DataFrame.
    """
    result = get_my_books(df_ratings, user_id)
    for _, row in df_user.iterrows():
        if row['ISBN'] not in result['ISBN'].tolist():
            new_row = {
                'user_id': user_id,
                'ISBN': row['ISBN'],
                'rating': row['rating']
            }
            df_new_row = pd.DataFrame([new_row])
            df_ratings = pd.concat([df_ratings, df_new_row], ignore_index=True)
        else:
            if not result.isin([row]).all(axis=1).any():
                df_ratings = add_rating(df_ratings, row, row['rating'])
    return df_ratings


def get_book_details(df_books: pd.DataFrame, isbn: str) -> dict:
    """
    Get details of a book by its ISBN.
    """
    book = df_books[df_books['ISBN'] == isbn].iloc[0]
    return {
        'title': book['title'],
        'author': book['author'],
        'publisher': book['publisher'],
        'image_url': book['image_url'],
        'avg_rating': book['avg_rating'],
        'num_ratings': book['num_ratings'],
    }


def display_books(df: pd.DataFrame, key_prefix: str):
    """
    Display books in a grid format with clickable buttons.
    """
    cols = cycle(st.columns(6))
    for _, row in df.iterrows():
        col = next(cols)
        with col:
            # Display image
            st.markdown(f"<img src='{row['image_url']}' width=200 height=300>", unsafe_allow_html=True)
            # Clickable button styled as text
            if col.button(f"{row['title']}", key=f"{key_prefix}_{row['ISBN']}", type="primary"):
                st.session_state.selected_book = row['ISBN']
                st.switch_page("pages/book_info.py")
