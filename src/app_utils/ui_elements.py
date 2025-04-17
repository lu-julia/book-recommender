"""
Functions to render UI elements for the app.
"""

import streamlit as st


def render_welcome_instructions() -> None:
    """
    Render a welcome message and instructions for using the app.
    """
    st.markdown(
        """
        <div style='display: flex; justify-content: center;'>
            <div style='background-color: #f9f9f9; padding: 20px; border-radius: 12px;
                        border: 1px solid #ddd; text-align: left;'>
                <h2 style='text-align: center; color: #2C3E50;'>
                    👋 Welcome to <span style='color: #1F618D;'>Your Next Read</span>!
                </h2>
                <p style='font-size: 16px; color: #34495E;'>
                    Looking for your next favorite book? You're in the right place!<br>
                    Just tell us what you've read, and we’ll do the rest –
                    recommending personalized book selections you’re likely to love.
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


def render_my_books_instructions():
    """
    Render instructions for the My Books page.
    """
    st.markdown(
        """
        <div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.75rem;
                    border-left: 5px solid #6c63ff;">
            <h4 style="margin-bottom: -6px; font-size: 18px; color: #2C3E50;">
                How to build your personalized reading profile:
            </h4>
            <ol style="color: #566573; font-size: 15px;">
                <li>Use the dropdown to search for books by title or author.</li>
                <li>Add books you've read to your list.</li>
                <li>Use the sliders to rate each book from 0 to 10.</li>
                <li>Don't forget to hit <strong>💾 Save books</strong> when you're done!</li>
            </ol>
            <p style="margin-top: 6px; margin-bottom: 6px; color: #34495E;">
                ✨ The more books you rate, the better your recommendations will be!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")


def style_text_button() -> None:
    """
    Style a button to make it look like text.
    """
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
