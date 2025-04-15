"""
Search page for the book recommendation app.
"""

import streamlit as st


def show():

    df_books = st.session_state.df_books.copy()

    # --- Session defaults for filters ---
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'year_from' not in st.session_state:
        st.session_state.year_from = int(df_books["year"].min())
    if 'year_to' not in st.session_state:
        st.session_state.year_to = int(df_books["year"].max())
    if 'sort_by' not in st.session_state:
        st.session_state.sort_by = "None"
    if 'page' not in st.session_state:
        st.session_state.page = 0

    # --- Search and filter options ---
    st.session_state.search_query = st.text_input(
        "Search by title or author",
        placeholder="Enter title or author name",
        value=st.session_state.search_query
    )

    with st.expander("🔧 Filters & Sorting", expanded=True):

        year_min = int(df_books["year"].min())
        year_max = int(df_books["year"].max())

        col1, col2, _, _, _ = st.columns(5)
        with col1:
            st.session_state.year_from = st.number_input(
                "Year from",
                min_value=year_min,
                max_value=year_max,
                value=st.session_state.year_from,
                key="year_from_input"
            )
        with col2:
            st.session_state.year_to = st.number_input(
                "Year to",
                min_value=year_min,
                max_value=year_max,
                value=st.session_state.year_to,
                key="year_to_input"
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
                "Number of ratings (Low to High)"
            ].index(st.session_state.sort_by),
            key="sort_by_select"
        )

        if st.button("🧹 Clear filters"):
            st.session_state.search_query = ""
            st.session_state.year_from = year_min
            st.session_state.year_to = year_max
            st.session_state.sort_by = "None"
            st.session_state.page = 0
            st.rerun()

    # --- Filtering ---
    if st.session_state.search_query:
        df_books = df_books[
            df_books["title"].str.contains(st.session_state.search_query, case=False, na=False)
            | df_books["author"].str.contains(st.session_state.search_query, case=False, na=False)
        ]

    if st.session_state.year_from > st.session_state.year_to:
        st.warning(f"Year to should be greater than {st.session_state.year_from}")
    else:
        df_books = df_books[
            df_books["year"].astype(int).between(st.session_state.year_from, st.session_state.year_to)
        ].sort_values("year", ascending=False)

    # --- Sorting ---
    if st.session_state.sort_by == "Rating (High to Low)":
        df_books = df_books.sort_values("avg_rating", ascending=False)
    elif st.session_state.sort_by == "Rating (Low to High)":
        df_books = df_books.sort_values("avg_rating", ascending=True)
    elif st.session_state.sort_by == "Number of ratings (High to Low)":
        df_books = df_books.sort_values("num_ratings", ascending=False)
    elif st.session_state.sort_by == "Number of ratings (Low to High)":
        df_books = df_books.sort_values("num_ratings", ascending=True)

    # --- Pagination ---
    per_page = 10
    total_pages = (len(df_books) - 1) // per_page + 1
    start = st.session_state.page * per_page
    end = start + per_page

    st.markdown(f"### 📚 Search Results ({len(df_books)} books found)")

    if not df_books.empty:
        for _, row in df_books.iloc[start:end].iterrows():
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

        # --- Navigation buttons ---
        col_prev, col_next = st.columns([1, 1])
        with col_prev:
            if st.session_state.page > 0:
                if st.button("⬅️ Previous"):
                    st.session_state.page -= 1
                    st.rerun()
        with col_next:
            if st.session_state.page < total_pages - 1:
                if st.button("Next ➡️"):
                    st.session_state.page += 1
                    st.rerun()
    else:
        st.info("No books found matching your search.")
