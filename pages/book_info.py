import streamlit as st

from src.app_utils.functions import get_book_details


def show():

    isbn = st.session_state['selected_book']
    st.write(f"Selected book: {isbn}")
    details = get_book_details(st.session_state.df_books, isbn)

    st.markdown("### 📘 Book Details")
    st.image(details['image_url'], width=150)
    st.write(f"**Title:** {details['title']}")
    st.write(f"**Author:** {details['author']}")
    st.write(f"**Publisher:** {details['publisher']}")
    st.write(f"**Average Rating:** {details['avg_rating']:.2f}" if details['avg_rating'] else "**Average Rating:** N/A")
    st.write(f"**Number of Ratings:** {details['num_ratings']}")

    if st.button("🔙 Back to Home"):
        st.switch_page("app.py")


if __name__ == "__main__":
    show()
