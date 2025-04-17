"""
Home page of the app.
"""

import streamlit as st
import pandas as pd

from src.recommendation.collaborative_filtering import cf_recommendation
from src.recommendation.popularity_based import (
    get_popular_books,
    get_books_from_authors,
)
from src.app_utils.functions import display_books


def show():
    if len(st.session_state.df_user) == 0:
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
            unsafe_allow_html=True,
        )

    else:
        if not st.session_state.saved:
            st.info("👉 Remember to hit the **Save books** button !")

        else:
            cols = st.columns([1, 0.05])

            with cols[0]:
                st.subheader("🎯 Your personalized recommendations")

            # Refresh button
            with cols[1]:
                if st.button("🔄", help="Refresh all recommendations", type="secondary"):
                    # Set a flag and delete all 3 cached sections
                    st.session_state["ratings_updated"] = True
                    for key in [
                        f"cf_recommendations_user_{st.session_state['user_id']}",
                        "popular_books",
                        "author_books",
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]

            # --- Colaborative filtering recommendations ---
            with st.spinner("Generating recommendations..."):
                # Define a key that changes only when new ratings are added
                cf_key = f"cf_recommendations_user_{st.session_state['user_id']}"

                # If not already in session state or user just updated ratings:
                if cf_key not in st.session_state or st.session_state.get(
                    "ratings_updated", False
                ):
                    recs_df = cf_recommendation(
                        st.session_state.df_ratings,
                        st.session_state.df_books,
                        st.session_state["user_id"],
                        n_reco=10,
                        n_factors=50,
                    )
                    st.session_state[cf_key] = recs_df.sample(6)
                    st.session_state["ratings_updated"] = False  # Reset flag after updating

                display_books(st.session_state[cf_key], key_prefix="cf")

                # Style override for button to make it look like text
                st.markdown(
                    """
                    <style>
                    button[kind="primary"] {
                        background: none!important;
                        border: none!important;
                        padding: 0!important;
                        color: black !important;
                        text-decoration: none;
                        cursor: pointer;
                        font-weight: 700  !important;
                        text-align: left !important;
                        display: block;
                        margin-top: 5px;
                    }
                    button[kind="primary"]:hover {
                        text-decoration: none;
                        color: #1F618D !important;
                    }
                    button[kind="primary"]:focus {
                        outline: none !important;
                        box-shadow: none !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )

                st.divider()

                # --- Popularity based recommendations ---
                st.subheader("📈 Most popular books")
                if "popular_books" not in st.session_state:
                    full_popular_df = get_popular_books(st.session_state.df_books)
                    st.session_state.popular_books = (
                        full_popular_df.sample(6)
                        if len(full_popular_df) > 6
                        else full_popular_df
                    )

                display_books(st.session_state.popular_books, key_prefix="pop")

                st.divider()

                # --- Author-based recommendations ---
                df_user_book = pd.merge(
                    st.session_state.df_user,
                    st.session_state.df_books,
                    on="ISBN",
                    how="left",
                )
                if "author_books" not in st.session_state:
                    full_author_df = get_books_from_authors(
                        df_user_book, st.session_state.df_books
                    )
                    st.session_state.author_books = (
                        full_author_df.sample(6)
                        if len(full_author_df) > 6
                        else full_author_df
                    )

                if not st.session_state.author_books.empty:
                    st.subheader("📚 More books from your favorite authors")
                    display_books(st.session_state.author_books, key_prefix="auth")
