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
from src.app_utils.ui_elements import (
    render_welcome_instructions,
    style_text_button,
)
from src.app_utils.functions import display_books


def show():
    if len(st.session_state.df_user) == 0:
        render_welcome_instructions()

    else:
        if not st.session_state.saved:
            st.warning("👉 Remember to hit the **💾 Save books** button !")
            render_welcome_instructions()

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
                style_text_button()

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
