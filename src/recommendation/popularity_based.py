"""
Module for popularity-based and author-based book recommendations.
"""

import pandas as pd


def get_popular_books(books_df: pd.DataFrame, n_books: int) -> pd.DataFrame:
    """
    Get popular books based on the number of ratings and average rating.

    Args:
        books_df (pd.DataFrame): DataFrame containing 'avg_rating' and 'num_ratings' columns.
        n_books (int): Number of popular books to return.

    Returns:
        pd.DataFrame: DataFrame containing popular books.
    """
    popular_books = books_df[(books_df["avg_rating"] >= 7) &
                             (books_df["num_ratings"] >= 100)]
    if len(popular_books) > n_books:
        return popular_books.sample(n_books)
    return popular_books


def get_books_from_authors(
        df_user_book: pd.DataFrame,
        books_df: pd.DataFrame,
        n_books: int,
    ) -> pd.DataFrame:
    """ 
    Get other books from specific authors.

    Args:
        df_user_book (pd.DataFrame): DataFrame of books rated by a user.
        books_df (pd.DataFrame): DataFrame containing books data and their ratings.
        n_books (int): Number of books to return.

    Returns:
        pd.DataFrame: DataFrame containing other books by the authors in df_user.
    """
    authors = df_user_book['author'].unique()
    exclude_isbns = df_user_book['ISBN'].unique()
    books_by_author = books_df[(books_df['author'].isin(authors)) &
                               (~books_df['ISBN'].isin(exclude_isbns))]
    if len(books_by_author) > n_books:
        return books_by_author.sample(n_books)
    return books_by_author
