"""
Search page for the book recommendation app.
"""

import streamlit as st


def show():
    books_df = st.session_state.df_books.copy()

    # --- Handle Clear button ---
    if st.session_state.filters_cleared:
        st.session_state.year_from = int(books_df["year"].min())
        st.session_state.year_to = int(books_df["year"].max())
        st.session_state.sort_by = "None"
        st.session_state.page = 0
        st.session_state.filters_cleared = False
        st.rerun()

    # --- Search and filter options ---
    st.session_state.search_query = st.text_input(
        "Search by title or author",
        placeholder="Enter title or author name",
        value=st.session_state.search_query,
    )

    with st.expander("🔧 Filters & Sorting", expanded=True):
        year_min = int(books_df["year"].min())
        year_max = int(books_df["year"].max())

        col1, col2, _, _, _ = st.columns(5)
        with col1:
            st.session_state.year_from = st.number_input(
                "Year from",
                min_value=year_min,
                max_value=year_max,
                value=st.session_state.year_from,
            )
        with col2:
            st.session_state.year_to = st.number_input(
                "Year to",
                min_value=year_min,
                max_value=year_max,
                value=st.session_state.year_to,
            )

        st.session_state.sort_by = st.selectbox(
            "Sort by",
            options=[
                "None",
                "Rating (High to Low)",
                "Rating (Low to High)",
                "Number of ratings (High to Low)",
                "Number of ratings (Low to High)",
            ],
            index=[
                "None",
                "Rating (High to Low)",
                "Rating (Low to High)",
                "Number of ratings (High to Low)",
                "Number of ratings (Low to High)",
            ].index(st.session_state.get("sort_by", "None")),
        )

        if st.button("🧹 Clear filters"):
            st.session_state.filters_cleared = True
            st.rerun()

    # --- Filtering ---
    if st.session_state.search_query:
        books_df = books_df[
            books_df["title"].str.contains(
                st.session_state.search_query, case=False, na=False
            )
            | books_df["author"].str.contains(
                st.session_state.search_query, case=False, na=False
            )
        ]

    books_df = books_df[
        books_df["year"]
        .astype(int)
        .between(st.session_state.year_from, st.session_state.year_to)
    ].sort_values("year", ascending=False)

    # --- Sorting ---
    if st.session_state.sort_by == "Rating (High to Low)":
        books_df = books_df.sort_values("avg_rating", ascending=False)
    elif st.session_state.sort_by == "Rating (Low to High)":
        books_df = books_df.sort_values("avg_rating", ascending=True)
    elif st.session_state.sort_by == "Number of ratings (High to Low)":
        books_df = books_df.sort_values("num_ratings", ascending=False)
    elif st.session_state.sort_by == "Number of ratings (Low to High)":
        books_df = books_df.sort_values("num_ratings", ascending=True)

    # --- Pagination ---
    books_per_page = 10
    total_books = len(books_df)
    total_pages = (total_books - 1) // books_per_page + 1
    start = st.session_state.page * books_per_page
    end = start + books_per_page

    # Ensure page index stays valid
    st.session_state.page = min(max(0, st.session_state.page), total_pages - 1)

    st.markdown(f"### 📚 Search Results ({total_books} books found)")

    # --- Display books ---
    if not books_df.empty:
        for _, row in books_df.iloc[start:end].iterrows():
            cols = st.columns([1, 4])
            with cols[0]:
                st.image(row["image_url"], width=100)
            with cols[1]:
                st.markdown(f"**{row['title']}**")
                st.markdown(f"By *{row['author']}* ({int(row['year'])})")
                st.markdown(
                    f"⭐ {row['avg_rating']:.1f} / 10 — {int(row['num_ratings'])} ratings"
                )
                if st.button("📖 See details", key=f"detail_{row['ISBN']}"):
                    st.session_state["selected_book"] = row["ISBN"]
                    st.session_state["previous_page"] = "search"
                    st.switch_page("pages/book_info.py")
            st.divider()

        # --- Pagination buttons ---
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.page > 0:
                if st.button("⬅️ Previous"):
                    st.session_state.page -= 1
                    st.rerun()
        with col2:
            st.markdown(
                f"<div style='text-align:center'>Page {st.session_state.page + 1} of {total_pages}</div>",
                unsafe_allow_html=True,
            )
        with col3:
            if st.session_state.page < total_pages - 1:
                if st.button("Next ➡️"):
                    st.session_state.page += 1
                    st.rerun()

    else:
        st.info("No books found matching your search.")
        if st.session_state.year_from > st.session_state.year_to:
            st.warning(
                f"""
                Please adjust the year range.
                Year from ({st.session_state.year_from}) should be less than or equal to Year to ({st.session_state.year_to}).
                """
            )
