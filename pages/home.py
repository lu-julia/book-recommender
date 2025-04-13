"""
Home page of the app.
"""

import streamlit as st
from itertools import cycle
import pandas as pd

from src.recommendation.collaborative_filtering import cf_recommendation
from src.recommendation.popularity_based import (
    get_popular_books,
    get_books_from_authors
)


def show():
    if (len(st.session_state.df_user)==0):
        st.markdown(
            """
            <div style='display: flex; justify-content: center;'>
                <div style='background-color: #f9f9f9; padding: 20px; border-radius: 12px; border: 1px solid #ddd; text-align: left;'>
                    <h2 style='text-align: center; color: #2C3E50;'>👋 Welcome to <span style='color: #1F618D;'>Your Next Read</span>!</h2>
                    <p style='font-size: 16px; color: #34495E;'>
                        Looking for your next favorite book? You're in the right place!<br>
                        Just tell us what you've read, and we’ll do the rest – recommending personalized book selections you’re likely to love.
                    </p>
                    <h4 style='color: #2C3E50;'>🛠️ How to use the app:</h4>
                    <ol style='color: #566573; font-size: 15px;'>
                        <li>Go to <strong>📚 My Books</strong> and rate a few books you've read.</li>
                        <li>Hit the <strong>💾 Save books</strong> button to update your preferences.</li>
                        <li>Return to <strong>🏠 Home</strong> to get your personalized recommendations.</li>
                        <li>Explore more using the <strong>🔍 Search</strong> tab to search books by title or author.</li>
                    </ol>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        if st.session_state.saved == False:
            st.info("👉 Remember to hit the **Save books** button !")

        else:
            # Book recommendations based on collaborative filtering
            st.subheader("🎯 Your personalized recomendations")
            recs_df = cf_recommendation(
                st.session_state.df_ratings,
                st.session_state.df_books,
                st.session_state['user_id'],
                n_reco=6,
                n_factors=100
            )
            cols = cycle(st.columns(6))
            for index in range(len(recs_df)):
                row = recs_df.iloc[index]
                col = next(cols)
                with col:
                    st.markdown(f"<img src='{row['image_url']}' width=200 height=300><br><b>{row['title']}</b>", unsafe_allow_html=True)
    
            st.divider()

            # Popularity based recommendations
            st.subheader("📈 Popular Books")
            popular_df = get_popular_books(st.session_state.df_books, n_books=6)
            cols = cycle(st.columns(6))
            for index in range(len(popular_df)):
                row = popular_df.iloc[index]
                col = next(cols)
                with col:
                    st.markdown(f"<img src='{row['image_url']}' width=200 height=300><br><b>{row['title']}</b>", unsafe_allow_html=True)

            st.divider()

            # Author-based recommendations
            df_user_book = pd.merge(st.session_state.df_user, st.session_state.df_books, on='ISBN', how='left')
            authors_df = get_books_from_authors(
                df_user_book,
                st.session_state.df_books,
                n_books=6
            )
            if len(authors_df) > 0:
                st.subheader("📚 Other books from your favorite authors")
                cols = cycle(st.columns(6))
                for index in range(len(authors_df)):
                    row = authors_df.iloc[index]
                    col = next(cols)
                    with col:
                        st.markdown(f"<img src='{row['image_url']}' width=200 height=300><br><b>{row['title']}</b>", unsafe_allow_html=True)
