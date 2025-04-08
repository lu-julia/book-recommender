"""
Functions to recommend books based on popularity.
"""

import pandas as pd


def get_popular_books(books_df: pd.DataFrame, n_books: int = 5) -> pd.DataFrame:
    """
    Get the top n popular books based on the number of ratings and average rating.

    Args:
        books_df (pd.DataFrame): DataFrame containing books data and their ratings.
        n_books (int): Number of popular books to return.

    Returns:
        pd.DataFrame: DataFrame containing the top n popular books with their average rating.
    """
    popular_books = books_df[
        books_df["num_ratings"] > 250
    ].sort_values("avg_rating", ascending=False)
    return popular_books.head(n_books)


def get_books_by_author(
        author: str,
        books_df: pd.DataFrame,
        exclude_isbns: list = [],
        n_books: int = 5
    ) -> pd.DataFrame:
    """ 
    Get books by a specific author, excluding certain ISBNs.

    Args:
        author (str): Name of the author.
        books_df (pd.DataFrame): DataFrame containing books data and their ratings.
        exclude_isbns (list): List of ISBNs to exclude from the results.
        n_books (int): Number of books to return.

    Returns:
        pd.DataFrame: DataFrame containing books by the specified author,
            sorted by the number of ratings.
    """
    books_by_author = books_df[(books_df['author']==author) &
                               (~books_df['ISBN'].isin(exclude_isbns))]
    return books_by_author.sort_values("num_ratings", ascending=False).head(n_books)
