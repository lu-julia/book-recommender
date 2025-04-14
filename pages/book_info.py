import streamlit as st

from src.app_utils.functions import get_book_details, get_star_rating


def show():
    isbn = st.session_state['selected_book']
    details = get_book_details(st.session_state.df_books, isbn)

    st.markdown("## 📘 Book Details")

    st.markdown(
        f"""
        <div style="display: flex; align-items: flex-start; gap: 32px; padding: 24px; background-color: #f9f9f9;
                    border: 1px solid #ddd; border-radius: 14px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05);">
            <div style="flex-shrink: 0;">
                <img src="{details['image_url']}" width="200" height="300" style="border-radius: 10px;">
            </div>
            <div style="flex: 1; color: #2C3E50;">
                <h2 style="margin-bottom: -6px;">{details['title']}</h2>
                <h3 style="font-size: 18px; margin-bottom: 8px; color: #555;"><em>by {details['author']}</em></h3>
                <p style="margin: 6px 0; font-size:18px;">{get_star_rating(details['avg_rating'])}</p>
                <p style="margin: 6px 0; margin-bottom: 16px;"><strong>👥 {details['num_ratings']} rating{'s' if details['num_ratings'] != 1 else ''}</strong></p>
                <p style="margin: 6px 0;"><strong>Year:</strong> {details['year']}</p>
                <p style="margin: 6px 0;"><strong>Publisher:</strong> {details['publisher']}</p>
                <p style="margin: 6px 0;"><strong>ISBN:</strong> {isbn}</p>
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("")


    if st.button("🔙 Back to Home"):
        st.switch_page("app.py")



if __name__ == "__main__":
    show()
