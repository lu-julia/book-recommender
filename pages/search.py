import streamlit as st
import pandas as pd


def show():
    books_df = st.session_state.df_books.copy()

    # Search and filter options
    search_query = st.text_input("Search by title or author", placeholder="Enter title or author name")

    year_min = int(books_df['year'].min())
    year_max = int(books_df['year'].max())

    col1, col2, _, _, _ = st.columns(5)
    with col1:
        year_from = st.number_input("Year from", min_value=year_min, max_value=year_max, value=year_min)
    with col2:
        year_to = st.number_input("Year to", min_value=year_min, max_value=year_max, value=year_max)

    # Filter dataframe
    if search_query:
        books_df = books_df[books_df["title"].str.contains(search_query, case=False, na=False) |
                            books_df["author"].str.contains(search_query, case=False, na=False)]
    books_df = books_df[
        books_df['year'].astype(int).between(year_from, year_to)
    ].sort_values(by='year', ascending=False)

    # Results
    st.markdown("### 📚 Search Results")
    if not books_df.empty:
        for _, row in books_df.head(20).iterrows():  # Limit to 20 results
            cols = st.columns([1, 4])
            with cols[0]:
                st.image(row['image_url'], width=100)
            with cols[1]:
                st.markdown(f"**{row['title']}**")
                st.markdown(f"By *{row['author']}* ({int(row['year'])})")
                st.markdown(f"⭐ {row['avg_rating']:.1f} / 10 — {int(row['num_ratings'])} ratings")
                # Book details
                if st.button("📖 See details", key=f"detail_{row['ISBN']}"):
                    st.session_state["selected_book"] = row["ISBN"]
                    st.session_state["previous_page"] = "search"
                    st.switch_page("pages/book_info.py")
            st.divider()
    else:
        st.info("No books found matching your search.")
