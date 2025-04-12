import streamlit as st
from itertools import cycle

from src.recommendation.collaborative_filtering import cf_recommendation


def show():
    if (len(st.session_state.df_user)==0):
        st.markdown("""
        ## 🏠 Welcome to the Book Recommender App
        ### 👋 How to use the app
        👉 Start by adding some books you’ve read !
        1. Go to **📚 My Books** and rate a few books you've read.
        2. Hit the **Save books** button.
        3. Come back to **🏠 Home** to see you personalized recommendations.
        4. Use **🔍 Search** to search for new books.
        """)

    else:
        if st.session_state.saved == False:
            st.markdown("""
            👉 Remember to hit the **Save books** button !
            """)
        else:
            st.markdown("### You might also like...")
            recs = cf_recommendation(st.session_state.df_ratings, st.session_state.df_books, st.session_state['user_id'], n_reco=8, n_factors=100)
            recs = recs[:6]
            cols = cycle(st.columns(6))
            for index in range(len(recs)):
                row = recs.iloc[index]
                col = next(cols)
                # Image
                img_markdown = f"<img src='{row['image_url']}' width={200} height={300}></a><figcaption>{row['title']}</figcaption>"
                col.markdown(img_markdown, unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📈 Popular Books and More")
    st.info("Coming soon: popular books, author-based recs... 🚀")